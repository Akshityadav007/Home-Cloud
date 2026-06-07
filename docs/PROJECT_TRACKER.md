
---

# 2. PROJECT_TRACKER.md

This is the MOST important file.

This tracks:
- completed tasks
- active tasks
- future roadmap
- blockers
- priorities

Think of it as:
> “Persistent engineering state.”

---

# Recommended Structure

```markdown id="y5k6f5"
# PROJECT TRACKER

---

# CURRENT STATUS

Project Phase:
FOUNDATION SETUP

Current Focus:
Backend infrastructure stabilization

Last Updated:
2026-06-07

---

# COMPLETED TASKS

## Project Initialization
- [x] Root project structure created
- [x] Frontend initialized using Next.js
- [x] Backend initialized using FastAPI
- [x] Docker Compose configured
- [x] PostgreSQL container setup
- [x] Redis container setup

## Backend Foundation
- [x] SQLAlchemy setup
- [x] Database connection established
- [x] User model created
- [x] Health route added
- [x] API versioning introduced
- [x] Environment config system added
- [x] Alembic initialized

---

# IN PROGRESS

## Backend Authentication
- [ ] Password hashing
- [ ] JWT token generation
- [ ] Login endpoint
- [ ] Register endpoint
- [ ] Refresh token system

---

# PENDING PHASES

## Phase 1 — Core Storage
- [ ] File upload
- [ ] File download
- [ ] Folder hierarchy
- [ ] File metadata management
- [ ] File deletion
- [ ] Search

## Phase 2 — Storage Engine
- [ ] Local storage provider
- [ ] Chunked uploads
- [ ] Resumable uploads
- [ ] File checksums
- [ ] Storage quotas

## Phase 3 — Security
- [ ] LUKS encrypted SSD
- [ ] HTTPS
- [ ] Secure file access
- [ ] Permission system

## Phase 4 — UI
- [ ] File explorer UI
- [ ] Upload progress UI
- [ ] Authentication pages

## Phase 5 — Advanced Features
- [ ] Sharing
- [ ] File versioning
- [ ] Thumbnails
- [ ] Background jobs
- [ ] Sync clients

---

# ARCHITECTURAL PRINCIPLES

- Modular monolith architecture
- Storage separated from metadata
- Local filesystem first
- Infrastructure simplicity prioritized
- Avoid premature distributed systems complexity

---

# FUTURE HARDWARE PLAN

Initial:
- Raspberry Pi
- Single encrypted SSD
- Single user

Future:
- Multi-user
- Dedicated NAS hardware
- RAID/ZFS
- Offsite backups

---

# KNOWN RISKS

- Raspberry Pi IO bottlenecks
- Sync engine complexity
- Storage corruption handling
- Backup strategy not yet implemented