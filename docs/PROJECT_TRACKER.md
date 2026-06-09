# PROJECT TRACKER

---

# CURRENT STATUS

Project Phase:
STORAGE LIFECYCLE & RECOVERY LAYER

Current Focus:
Batch operations + recovery lifecycle foundation

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
* [x] Folder contents API
* [x] Root-level navigation API

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
* [x] Checksum-based integrity tracking added

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
* [x] Temporary upload staging introduced
* [x] Atomic-ish file move strategy introduced
* [x] SHA256 checksum generation implemented
* [x] Streamed checksum calculation implemented

---

## Multi-file Upload System

* [x] Multi-file upload endpoint
* [x] Sequential upload processing
* [x] Shared folder upload support
* [x] Upload logic reuse through service abstraction
* [x] Batch multipart upload support

---

## Download Pipeline

* [x] Secure file download endpoint
* [x] File retrieval authorization
* [x] Safe streaming response handling
* [x] Download response headers
* [x] File existence validation
* [x] Ownership-protected downloads
* [x] StreamingResponse integration
* [x] Download pipeline tested successfully

---

## Soft Delete Architecture

* [x] `deleted_at` strategy introduced
* [x] Logical deletion implemented
* [x] Deleted file filtering added to repositories
* [x] Search exclusion for deleted files
* [x] Navigation exclusion for deleted files
* [x] Download blocking for deleted files
* [x] Soft-delete lifecycle tested successfully

---

## Batch File Operations

* [x] Batch soft-delete endpoint
* [x] Partial success deletion handling
* [x] Multi-file ownership validation
* [x] Batch deletion response model
* [x] Batch deletion lifecycle tested

---

## Navigation & Query Layer

* [x] Folder-specific file listing
* [x] Folder navigation APIs
* [x] Root-level navigation APIs
* [x] Combined folder/file response model
* [x] File search APIs
* [x] Case-insensitive filename search
* [x] User-isolated search results
* [x] Query validation
* [x] Improved virtual filesystem navigation

---

# IN PROGRESS

## Storage Recovery & Cleanup Lifecycle

* [ ] Trash recovery architecture
* [ ] Background cleanup architecture
* [ ] Upload interruption recovery strategy
* [ ] Orphan file reconciliation planning
* [ ] Soft-delete cleanup lifecycle

---

# PENDING PHASES

## Phase 1 — Core Storage

* [x] File upload
* [x] File download
* [x] File metadata management
* [x] File deletion
* [x] Search
* [x] Multi-file uploads
* [x] Batch file deletion

---

## Phase 2 — Storage Engine

* [ ] Chunked uploads
* [ ] Resumable uploads
* [x] File checksums
* [ ] Storage quotas
* [ ] Storage cleanup jobs
* [ ] Thumbnail generation
* [ ] Move storage root path into environment config
* [x] Temporary upload staging system
* [ ] Orphan file cleanup process
* [ ] Multi-disk storage orchestration
* [ ] Background consistency repair jobs
* [ ] Trash recovery system
* [ ] Multiple file download system
* [ ] Zip archive streaming
* [ ] Temporary archive cleanup jobs

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
* [ ] Mobile-first filesystem UX
* [ ] Trash bin UI

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

# NEXT IMMEDIATE GOALS

1. Trash recovery system
2. Restore deleted files endpoint
3. Background cleanup architecture
4. Upload recovery improvements
5. Begin Flutter client initialization

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
* File operations secured through ownership-based authorization
* Navigation APIs modeled after real filesystem traversal
* Soft-delete chosen over immediate hard delete
* Batch operations designed with partial-success semantics
