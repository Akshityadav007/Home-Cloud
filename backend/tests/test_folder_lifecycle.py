from io import BytesIO


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


def test_folder_delete_restore_and_permanent_delete_are_recursive(client):
    token = _register_and_login(client, "folder-life@example.com")
    headers = _auth_headers(token)

    root_response = client.post(
        "/api/v1/folders/",
        json={
            "name": "Documents"
        },
        headers=headers
    )
    root_id = root_response.json()["id"]

    child_response = client.post(
        "/api/v1/folders/",
        json={
            "name": "Receipts",
            "parent_folder_id": root_id
        },
        headers=headers
    )
    child_id = child_response.json()["id"]

    upload_response = client.post(
        "/api/v1/files/upload",
        data={
            "folder_id": str(child_id)
        },
        files={
            "file": ("receipt.txt", BytesIO(b"receipt"), "text/plain")
        },
        headers=headers
    )
    file_id = upload_response.json()["id"]

    delete_response = client.delete(
        f"/api/v1/folders/{root_id}",
        headers=headers
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["folders_deleted"] == 2
    assert delete_response.json()["files_deleted"] == 1

    assert client.get(
        "/api/v1/folders/root/contents",
        headers=headers
    ).json()["folders"] == []

    assert client.get(
        f"/api/v1/files/{file_id}/download",
        headers=headers
    ).status_code == 404

    restore_response = client.post(
        f"/api/v1/folders/{root_id}/restore",
        headers=headers
    )

    assert restore_response.status_code == 200

    root_contents = client.get(
        "/api/v1/folders/root/contents",
        headers=headers
    ).json()
    assert root_contents["folders"][0]["id"] == root_id

    child_contents = client.get(
        f"/api/v1/folders/{root_id}/contents",
        headers=headers
    ).json()
    assert child_contents["folders"][0]["id"] == child_id

    assert client.get(
        f"/api/v1/files/{file_id}/download",
        headers=headers
    ).status_code == 200

    permanent_response = client.post(
        f"/api/v1/folders/{root_id}/permanent-delete",
        headers=headers
    )

    assert permanent_response.status_code == 200
    assert client.post(
        f"/api/v1/folders/{root_id}/restore",
        headers=headers
    ).status_code == 404
    assert client.get(
        "/api/v1/folders/trash",
        headers=headers
    ).json() == []


def test_deleted_parent_folder_cannot_receive_new_child_or_upload(client):
    token = _register_and_login(client, "deleted-parent@example.com")
    headers = _auth_headers(token)

    folder_response = client.post(
        "/api/v1/folders/",
        json={
            "name": "Archive"
        },
        headers=headers
    )
    folder_id = folder_response.json()["id"]

    client.delete(
        f"/api/v1/folders/{folder_id}",
        headers=headers
    )

    child_response = client.post(
        "/api/v1/folders/",
        json={
            "name": "Blocked",
            "parent_folder_id": folder_id
        },
        headers=headers
    )

    upload_response = client.post(
        "/api/v1/files/upload",
        data={
            "folder_id": str(folder_id)
        },
        files={
            "file": ("blocked.txt", BytesIO(b"blocked"), "text/plain")
        },
        headers=headers
    )

    assert child_response.status_code == 404
    assert upload_response.status_code == 404
