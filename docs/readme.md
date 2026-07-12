To run the website use:
1) Frontend - This will be an app.
2) Backend - cd backend > uvicorn app.main:app --reload

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

## Folder Lifecycle API

- `DELETE /api/v1/folders/{folder_id}` soft-deletes a folder subtree and contained files.
- `GET /api/v1/folders/trash` lists deleted folders that are still recoverable.
- `POST /api/v1/folders/{folder_id}/restore` restores a deleted folder subtree and contained files.
- `POST /api/v1/folders/{folder_id}/permanent-delete` marks a folder subtree and contained files as permanently deleted.

---

## Local Development Setup

### Start Infra

```bash
docker compose up -d
