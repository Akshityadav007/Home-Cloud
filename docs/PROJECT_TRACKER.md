# PROJECT TRACKER

---

# CURRENT STATUS

Project Phase:
CORE STORAGE IMPLEMENTATION

Current Focus:
Secure upload pipeline + file metadata integration

Last Updated:
2026-06-08

---

# COMPLETED TASKS

## Project Initialization

* [x] Root project structure created
* [x] Frontend initialized using Next.js
* [x] Backend initialized using FastAPI
* [x] Docker Compose configured
* [x] PostgreSQL container setup
* [x] Redis container setup

---

## Backend Foundation

* [x] SQLAlchemy setup
* [x] Database connection established
* [x] User model created
* [x] Health route added
* [x] API versioning introduced
* [x] Environment config system added
* [x] Alembic initialized
* [x] Alembic migrations working
* [x] Dependency injection setup
* [x] Repository layer introduced
* [x] Service layer introduced

---

## Authentication System

* [x] Password hashing
* [x] JWT token generation
* [x] Register endpoint
* [x] Login endpoint
* [x] Protected route dependency
* [x] Current authenticated user resolution (`/me`)
* [x] Postman authentication workflow tested

---

## Folder System

* [x] Folder model created
* [x] Nested folder hierarchy support
* [x] Folder ownership validation
* [x] Create folder endpoint
* [x] List folders endpoint
* [x] Parent-child folder validation
* [x] Folder authentication protection

---

## Storage Preparation

* [x] Storage abstraction architecture planned

* [x] Physical storage directory structure initialized

* [x] Separation established between:

  * application storage code
  * physical file storage

* [x] Storage path auto-creation logic added

* [x] Path resolution stabilized using `Path(__file__).resolve()`

---

## Storage Engine Foundation

* [x] Storage provider interface
* [x] Local filesystem storage provider
* [x] Safe UUID filename generation
* [x] Directory sharding strategy implemented
* [x] File metadata model
* [x] File repository created
* [x] File service layer created
* [x] File routes initialized
* [x] File ownership model established

---

## Upload Pipeline

* [x] Secure authenticated upload endpoint
* [x] Multipart form upload support
* [x] Folder-linked uploads
* [x] Ownership validation during uploads
* [x] Physical file persistence
* [x] Metadata persistence
* [x] MIME type persistence
* [x] File size persistence
* [x] Upload pipeline tested successfully

---

# IN PROGRESS

## File Access Layer

* [ ] Secure file download endpoint
* [ ] File retrieval authorization
* [ ] Safe streaming response handling
* [ ] Download response headers
* [ ] File existence validation

---

# PENDING PHASES

## Phase 1 — Core Storage

* [x] File upload
* [ ] File download
* [x] File metadata management
* [ ] File deletion
* [ ] Search

---

## Phase 2 — Storage Engine

* [ ] Chunked uploads
* [ ] Resumable uploads
* [ ] File checksums
* [ ] Storage quotas
* [ ] Multi-file uploads
* [ ] Storage cleanup jobs
* [ ] Thumbnail generation
* [ ] Move storage root path into environment config
* [ ] Temporary upload staging system
* [ ] Orphan file cleanup process

---

## Phase 3 — Security

* [ ] LUKS encrypted SSD
* [ ] HTTPS
* [ ] Secure file access
* [ ] Permission system
* [ ] File access auditing
* [ ] Rate limiting
* [ ] Upload validation
* [ ] Malware scanning

---

## Phase 4 — UI

* [ ] Flutter mobile application initialization
* [ ] Authentication screens
* [ ] File explorer UI
* [ ] Upload progress UI
* [ ] Folder navigation UI
* [ ] Drag-and-drop uploads
* [ ] Offline caching strategy

---

## Phase 5 — Advanced Features

* [ ] Sharing
* [ ] File versioning
* [ ] Background jobs
* [ ] Sync clients
* [ ] Multi-device support
* [ ] Conflict resolution system
* [ ] Cross-device synchronization

---

# CURRENT ARCHITECTURE

## Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* Redis
* Alembic
* JWT Authentication

---

## Frontend Direction

* Flutter planned as primary client platform
* Mobile-first architecture
* API-first backend design

---

## Infrastructure

* Docker Compose
* Local filesystem storage
* Raspberry Pi deployment target
* Future encrypted SSD storage

---

# ARCHITECTURAL PRINCIPLES

* Modular monolith architecture
* Storage separated from metadata
* Local filesystem first
* Infrastructure simplicity prioritized
* Avoid premature distributed systems complexity
* Separate application code from physical user data
* Repository-service architecture enforced
* API-first design for long-term mobile compatibility

---

# STORAGE ARCHITECTURE

## Application Storage Layer

Location:
`backend/app/storage/`

Purpose:

* Storage provider interfaces
* Local storage provider implementation
* Future storage backends
* File handling utilities

---

## Physical Storage Layer

Location:
`root/storage/`

Purpose:

* Actual uploaded files
* Upload chunks
* Temporary files
* Generated thumbnails

---

# FUTURE HARDWARE PLAN

Initial:

* Raspberry Pi
* Single encrypted SSD
* Single user

Future:

* Multi-user
* User-specific storage quotas
* Additional external storage devices
* Dedicated NAS hardware
* RAID/ZFS
* Offsite backups

---

# KNOWN RISKS

* Raspberry Pi IO bottlenecks
* Sync engine complexity
* Storage corruption handling
* Backup strategy not yet implemented
* Physical disk failure
* File consistency guarantees not yet implemented
* Upload interruption consistency handling pending

---

# CONSISTENCY & DURABILITY NOTES

Current State:

* PostgreSQL provides ACID guarantees for metadata
* Filesystem writes are not yet fully transactional

Future Improvements Planned:

* Temporary upload staging
* Atomic file move operations
* Upload integrity verification
* Orphan file cleanup jobs
* Checksum validation
* Recovery workflows after interruption/power loss

---

# NEXT IMMEDIATE GOALS

1. Implement secure file download pipeline
2. Add file retrieval authorization
3. Add streaming download responses
4. Add secure file deletion flow
5. Introduce upload integrity validation

---

# IMPORTANT DESIGN DECISIONS

* Filesystem chosen over object storage initially
* Modular monolith chosen over microservices
* Local-first storage strategy
* Flat folder listing initially instead of recursive tree APIs
* Authentication completed before file uploads
* Folder hierarchy completed before storage engine
* Physical file storage separated from metadata layer
* Flutter selected as long-term frontend direction
* Storage provider abstraction introduced before uploads