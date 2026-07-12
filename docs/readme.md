To run the backend server:
1) Start infrastructure: `docker compose up -d`
2) Backend: `cd backend`
3) Activate a working venv.
4) Run: `uvicorn app.main:app --reload`

To generate JWT secret key use:
- python -c "import secrets; print(secrets.token_hex(32))"
-------------------------------------------------------------------------------------

# Cloud Storage System

## Overview

Private self-hosted cloud storage platform for long-term personal/family use.

Primary goals:
- Full ownership of data
- Modular scalable architecture
- Self-hosted infrastructure
- Zero third-party dependency for core storage
- Long-term maintainability

---

## Current Architecture

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- Redis
- Alembic

### Frontend
- Flutter mobile app planned

### Infrastructure
- Docker Compose
- Raspberry Pi deployment target
- Encrypted SSD storage (planned)

---

## Current Features

- Backend initialized
- PostgreSQL integration
- Redis integration
- Alembic migrations
- User model
- Authenticated folder and file APIs
- Soft-delete, restore, and permanent-delete lifecycle for files
- Recursive soft-delete, restore, and permanent-delete lifecycle for folders
- Multi-file upload and ZIP archive download
- Configurable max upload size and per-user storage quota
- Physical cleanup endpoint for permanently deleted files
- Backend regression test suite
- Chunked and resumable uploads
- File versioning
- Sharing and permission foundation
- Device sync events and conflict detection
- Audit logs, rate limiting, and malware-scan hook
- Thumbnail generation for images
- Storage consistency and orphan cleanup

## Folder Lifecycle API

- `DELETE /api/v1/folders/{folder_id}` soft-deletes a folder subtree and contained files.
- `GET /api/v1/folders/trash` lists deleted folders that are still recoverable.
- `POST /api/v1/folders/{folder_id}/restore` restores a deleted folder subtree and contained files.
- `POST /api/v1/folders/{folder_id}/permanent-delete` marks a folder subtree and contained files as permanently deleted.

## File Utility API

- `POST /api/v1/files/download-archive` streams selected files as a ZIP archive.
- `POST /api/v1/files/cleanup/permanent-deletes` removes physical files already marked as permanently deleted.
- `POST /api/v1/uploads/sessions` starts a resumable chunked upload.
- `POST /api/v1/uploads/sessions/{session_id}/chunks/{chunk_index}` uploads a chunk.
- `POST /api/v1/uploads/sessions/{session_id}/finalize` finalizes a complete upload.
- `POST /api/v1/files/{file_id}/thumbnail` generates an image thumbnail.

## Advanced API

- `POST /api/v1/files/{file_id}/shares` creates a file share.
- `GET /api/v1/shared/{token}/download` downloads a shared file.
- `GET /api/v1/files/{file_id}/versions` lists versions.
- `POST /api/v1/files/{file_id}/versions` uploads a new version.
- `POST /api/v1/devices` registers a sync device.
- `GET /api/v1/sync/events` returns sync events.
- `POST /api/v1/sync/conflicts/resolve` detects client/server conflicts.
- `GET /api/v1/audit` returns user audit logs.
- `GET /api/v1/storage/consistency` reports missing/orphaned storage.
- `POST /api/v1/storage/cleanup-orphans` removes orphaned physical files.

## Production Hardware

Recommended owned setup:

- Used mini PC for the backend server.
- External SSD for live storage.
- External HDD for cheapest backup storage.
- Small UPS for mini PC, SSD, HDD, and router.
- Self-managed WireGuard VPN for private remote access, or owned HTTPS reverse proxy if public access is required.

Avoid depending on a closed relay service if full network visibility is required.

---

## Local Development Setup

### Start Infra

```bash
docker compose up -d
