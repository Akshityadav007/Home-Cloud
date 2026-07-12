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


def test_users_cannot_access_each_others_folders_or_files(client):
    owner_token = _register_and_login(client, "owner@example.com")
    intruder_token = _register_and_login(client, "intruder@example.com")
    owner_headers = _auth_headers(owner_token)
    intruder_headers = _auth_headers(intruder_token)

    folder_response = client.post(
        "/api/v1/folders/",
        json={
            "name": "Private"
        },
        headers=owner_headers
    )
    folder_id = folder_response.json()["id"]

    upload_response = client.post(
        "/api/v1/files/upload",
        data={
            "folder_id": str(folder_id)
        },
        files={
            "file": ("secret.txt", BytesIO(b"secret"), "text/plain")
        },
        headers=owner_headers
    )
    file_id = upload_response.json()["id"]

    assert client.get(
        f"/api/v1/folders/{folder_id}/contents",
        headers=intruder_headers
    ).status_code == 403

    assert client.post(
        "/api/v1/folders/",
        json={
            "name": "Blocked",
            "parent_folder_id": folder_id
        },
        headers=intruder_headers
    ).status_code == 404

    assert client.post(
        "/api/v1/files/upload",
        data={
            "folder_id": str(folder_id)
        },
        files={
            "file": ("blocked.txt", BytesIO(b"blocked"), "text/plain")
        },
        headers=intruder_headers
    ).status_code == 404

    assert client.get(
        f"/api/v1/files/{file_id}/download",
        headers=intruder_headers
    ).status_code == 404

    assert client.delete(
        f"/api/v1/files/{file_id}",
        headers=intruder_headers
    ).status_code == 404

    assert client.delete(
        f"/api/v1/folders/{folder_id}",
        headers=intruder_headers
    ).status_code == 404
