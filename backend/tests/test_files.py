from io import BytesIO
import zipfile
from app.core.config import settings


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


def test_upload_download_search_delete_restore_lifecycle(client):
    token = _register_and_login(client, "upload-life@example.com")
    headers = _auth_headers(token)

    folder_response = client.post(
        "/api/v1/folders/",
        json={
            "name": "Uploads"
        },
        headers=headers
    )
    folder_id = folder_response.json()["id"]

    upload_response = client.post(
        "/api/v1/files/upload",
        data={
            "folder_id": str(folder_id)
        },
        files={
            "file": ("notes.txt", BytesIO(b"hello cloud"), "text/plain")
        },
        headers=headers
    )

    assert upload_response.status_code == 200
    uploaded = upload_response.json()
    assert uploaded["original_filename"] == "notes.txt"
    assert uploaded["folder_id"] == folder_id
    assert uploaded["size_bytes"] == 11
    assert uploaded["checksum"]

    file_id = uploaded["id"]

    download_response = client.get(
        f"/api/v1/files/{file_id}/download",
        headers=headers
    )
    assert download_response.status_code == 200
    assert download_response.content == b"hello cloud"

    search_response = client.get(
        "/api/v1/files/search?q=notes",
        headers=headers
    )
    assert search_response.status_code == 200
    assert search_response.json()[0]["id"] == file_id

    delete_response = client.delete(
        f"/api/v1/files/{file_id}",
        headers=headers
    )
    assert delete_response.status_code == 200

    assert client.get(
        f"/api/v1/files/{file_id}/download",
        headers=headers
    ).status_code == 404

    trash_response = client.get(
        "/api/v1/files/trash",
        headers=headers
    )
    assert trash_response.status_code == 200
    assert trash_response.json()[0]["id"] == file_id

    restore_response = client.post(
        f"/api/v1/files/{file_id}/restore",
        headers=headers
    )
    assert restore_response.status_code == 200

    assert client.get(
        f"/api/v1/files/{file_id}/download",
        headers=headers
    ).status_code == 200


def test_multi_file_upload_and_batch_lifecycle(client):
    token = _register_and_login(client, "batch-life@example.com")
    headers = _auth_headers(token)

    upload_response = client.post(
        "/api/v1/files/upload-multiple",
        files=[
            ("files", ("a.txt", BytesIO(b"a"), "text/plain")),
            ("files", ("b.txt", BytesIO(b"b"), "text/plain"))
        ],
        headers=headers
    )

    assert upload_response.status_code == 200
    file_ids = [file["id"] for file in upload_response.json()]

    delete_response = client.post(
        "/api/v1/files/batch-delete",
        json={
            "file_ids": [file_ids[0], file_ids[1], 9999]
        },
        headers=headers
    )
    assert delete_response.json() == {
        "deleted": file_ids,
        "failed": [9999]
    }

    restore_response = client.post(
        "/api/v1/files/batch-restore",
        json={
            "file_ids": file_ids
        },
        headers=headers
    )
    assert restore_response.json() == {
        "restored": file_ids,
        "failed": []
    }

    permanent_response = client.post(
        "/api/v1/files/batch-permanent-delete",
        json={
            "file_ids": file_ids
        },
        headers=headers
    )
    assert permanent_response.json() == {
        "deleted": file_ids,
        "failed": []
    }


def test_archive_download_includes_requested_files(client):
    token = _register_and_login(client, "archive@example.com")
    headers = _auth_headers(token)

    upload_response = client.post(
        "/api/v1/files/upload-multiple",
        files=[
            ("files", ("a.txt", BytesIO(b"alpha"), "text/plain")),
            ("files", ("b.txt", BytesIO(b"beta"), "text/plain"))
        ],
        headers=headers
    )

    file_ids = [file["id"] for file in upload_response.json()]

    archive_response = client.post(
        "/api/v1/files/download-archive",
        json={
            "file_ids": file_ids
        },
        headers=headers
    )

    assert archive_response.status_code == 200
    assert archive_response.headers["content-type"] == "application/zip"

    with zipfile.ZipFile(BytesIO(archive_response.content)) as archive:
        assert archive.read("a.txt") == b"alpha"
        assert archive.read("b.txt") == b"beta"


def test_upload_limits_reject_oversized_file_and_quota_excess(client, monkeypatch):
    token = _register_and_login(client, "limits@example.com")
    headers = _auth_headers(token)

    monkeypatch.setattr(settings, "MAX_UPLOAD_SIZE_BYTES", 3)

    too_large_response = client.post(
        "/api/v1/files/upload",
        files={
            "file": ("large.txt", BytesIO(b"large"), "text/plain")
        },
        headers=headers
    )

    assert too_large_response.status_code == 413

    monkeypatch.setattr(settings, "MAX_UPLOAD_SIZE_BYTES", 0)
    monkeypatch.setattr(settings, "USER_STORAGE_QUOTA_BYTES", 5)

    first_response = client.post(
        "/api/v1/files/upload",
        files={
            "file": ("first.txt", BytesIO(b"1234"), "text/plain")
        },
        headers=headers
    )
    second_response = client.post(
        "/api/v1/files/upload",
        files={
            "file": ("second.txt", BytesIO(b"12"), "text/plain")
        },
        headers=headers
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 413


def test_cleanup_permanently_deleted_files_removes_physical_file(client):
    token = _register_and_login(client, "cleanup@example.com")
    headers = _auth_headers(token)

    upload_response = client.post(
        "/api/v1/files/upload",
        files={
            "file": ("remove.txt", BytesIO(b"remove"), "text/plain")
        },
        headers=headers
    )
    file_id = upload_response.json()["id"]

    permanent_response = client.post(
        f"/api/v1/files/{file_id}/permanent-delete",
        headers=headers
    )
    assert permanent_response.status_code == 200

    cleanup_response = client.post(
        "/api/v1/files/cleanup/permanent-deletes",
        headers=headers
    )

    assert cleanup_response.status_code == 200
    assert cleanup_response.json() == {
        "removed": [file_id],
        "missing": []
    }
