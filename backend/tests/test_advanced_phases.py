from io import BytesIO
from PIL import Image


def _register_and_login(client, email):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "password123"
        }
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "password123"
        }
    )

    return response.json()["access_token"]


def _auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def _upload_file(
    client,
    headers,
    name="file.txt",
    content=b"hello",
    mime_type="text/plain"
    ):
    response = client.post(
        "/api/v1/files/upload",
        files={
            "file": (name, BytesIO(content), mime_type)
        },
        headers=headers
    )
    assert response.status_code == 200
    return response.json()


def test_chunked_upload_share_audit_and_sync_flow(client):
    token = _register_and_login(client, "advanced@example.com")
    headers = _auth_headers(token)

    session_response = client.post(
        "/api/v1/uploads/sessions",
        json={
            "original_filename": "chunked.txt",
            "mime_type": "text/plain",
            "total_size": 10,
            "chunk_size": 5
        },
        headers=headers
    )
    assert session_response.status_code == 200
    session_id = session_response.json()["id"]

    for index, content in enumerate([b"hello", b"world"]):
        chunk_response = client.post(
            f"/api/v1/uploads/sessions/{session_id}/chunks/{index}",
            files={
                "chunk": ("chunk.part", BytesIO(content), "application/octet-stream")
            },
            headers=headers
        )
        assert chunk_response.status_code == 200

    finalize_response = client.post(
        f"/api/v1/uploads/sessions/{session_id}/finalize",
        headers=headers
    )
    assert finalize_response.status_code == 200
    file_id = finalize_response.json()["id"]

    share_response = client.post(
        f"/api/v1/files/{file_id}/shares",
        json={
            "permission": "read"
        },
        headers=headers
    )
    assert share_response.status_code == 200
    token_value = share_response.json()["token"]

    shared_download = client.get(
        f"/api/v1/shared/{token_value}/download"
    )
    assert shared_download.status_code == 200
    assert shared_download.content == b"helloworld"

    events_response = client.get(
        "/api/v1/sync/events",
        headers=headers
    )
    assert events_response.status_code == 200
    assert any(event["event_type"] == "created" for event in events_response.json())

    audit_response = client.get(
        "/api/v1/audit",
        headers=headers
    )
    assert audit_response.status_code == 200
    assert any(log["action"] == "share_created" for log in audit_response.json())


def test_versions_devices_conflicts_and_storage_consistency(client):
    token = _register_and_login(client, "sync@example.com")
    headers = _auth_headers(token)
    uploaded = _upload_file(client, headers, "versioned.txt", b"v1")
    file_id = uploaded["id"]

    version_response = client.post(
        f"/api/v1/files/{file_id}/versions",
        files={
            "upload": ("versioned.txt", BytesIO(b"v2"), "text/plain")
        },
        headers=headers
    )
    assert version_response.status_code == 200
    assert version_response.json()["version_number"] == 2

    versions_response = client.get(
        f"/api/v1/files/{file_id}/versions",
        headers=headers
    )
    assert versions_response.status_code == 200
    assert len(versions_response.json()) == 2

    device_response = client.post(
        "/api/v1/devices",
        json={
            "client_id": "phone-1",
            "name": "Phone"
        },
        headers=headers
    )
    assert device_response.status_code == 200

    conflict_response = client.post(
        "/api/v1/sync/conflicts/resolve",
        json={
            "file_id": file_id,
            "client_checksum": "not-the-server-checksum"
        },
        headers=headers
    )
    assert conflict_response.status_code == 200
    assert conflict_response.json()["has_conflict"] is True

    consistency_response = client.get(
        "/api/v1/storage/consistency",
        headers=headers
    )
    assert consistency_response.status_code == 200
    assert consistency_response.json()["missing_physical_files"] == []


def test_malware_extension_policy_blocks_dangerous_upload(client):
    token = _register_and_login(client, "security@example.com")
    headers = _auth_headers(token)

    response = client.post(
        "/api/v1/files/upload",
        files={
            "file": ("bad.exe", BytesIO(b"not really executable"), "application/octet-stream")
        },
        headers=headers
    )

    assert response.status_code == 400


def test_thumbnail_generation_for_image_upload(client):
    token = _register_and_login(client, "thumb@example.com")
    headers = _auth_headers(token)
    image_bytes = BytesIO()
    Image.new("RGB", (32, 32), color="blue").save(image_bytes, format="PNG")
    image_bytes.seek(0)

    uploaded = _upload_file(
        client,
        headers,
        "image.png",
        image_bytes.read(),
        "image/png"
    )

    response = client.post(
        f"/api/v1/files/{uploaded['id']}/thumbnail",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["file_id"] == uploaded["id"]
    assert response.json()["thumbnail_path"].endswith(".jpg")
