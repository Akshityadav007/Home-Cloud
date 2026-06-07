To run the website use:
1) Frontend - cd frontend > npm run dev
2) Backend - cd backend > uvicorn app.main:app --reload
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
- Next.js
- TailwindCSS

### Infrastructure
- Docker Compose
- Raspberry Pi deployment target
- Encrypted SSD storage (planned)

---

## Current Features

- Backend initialized
- Frontend initialized
- PostgreSQL integration
- Redis integration
- Alembic migrations
- User model

---

## Local Development Setup

### Start Infra

```bash
docker compose up -d