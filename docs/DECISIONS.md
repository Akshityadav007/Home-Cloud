# ARCHITECTURAL DECISIONS

---

## Decision 001

Date:
2026-06-07

Title:
Use Modular Monolith Instead of Microservices

Reason:
Current scale is single-user and single-node.
Microservices would introduce unnecessary deployment and operational complexity.

Consequences:

* Faster development
* Easier debugging
* Simpler deployment
* Easier transactions

Future Reconsideration:
Revisit only if scaling beyond single-machine architecture.

---

## Decision 002

Date:
2026-06-07

Title:
Use Local Filesystem Instead of Object Storage

Reason:
Current infrastructure is single SSD attached to Raspberry Pi.
Filesystem access is simpler and lower overhead.

Consequences:

* Easier implementation
* Faster iteration
* Simpler debugging

Future Reconsideration:
Possible migration to MinIO/S3 abstraction layer later.

---

## Decision 003

Date:
2026-06-07

Title:
Use FastAPI Backend

Reason:
Strong Python ecosystem familiarity and good async support.
Fits future AI/data infrastructure integrations.

Consequences:

* Rapid development
* Strong typing with Pydantic
* Easy API documentation

---

## Decision 004

Date:
2026-06-08

Title:
Use Storage Provider Abstraction Layer

Reason:
Physical storage implementation should remain decoupled from business logic.

Consequences:

* Easier future migration to S3/MinIO
* Cleaner filesystem encapsulation
* Centralized storage handling
* Easier testing

Future Reconsideration:
Possibly evolve into pluggable provider registry.

---

## Decision 005

Date:
2026-06-08

Title:
Use UUID-based Physical Filenames

Reason:
Client-provided filenames are unsafe and collision-prone.

Consequences:

* Prevents filename collisions
* Prevents path traversal risks
* Allows duplicate original filenames safely

Future Reconsideration:
Potential hybrid content-addressed storage later.

---

## Decision 006

Date:
2026-06-08

Title:
Use Directory Sharding Strategy

Reason:
Large flat directories degrade filesystem performance over time.

Consequences:

* Better filesystem scalability
* Lower directory lookup overhead
* More maintainable storage structure

Future Reconsideration:
May evolve toward hashed object storage layout.

---

## Decision 007

Date:
2026-06-08

Title:
Use Flutter as Primary Frontend Platform

Reason:
Project is mobile-first and maintaining both web + mobile separately would increase operational overhead significantly.

Consequences:

* Single mobile-focused codebase
* Easier offline support
* Better native file handling
* Faster solo development velocity

Future Reconsideration:
Possible lightweight admin web portal later.

---

## Decision 008

Date:
2026-06-08

Title:
Use Real Filesystem Navigation APIs Instead of Recursive Tree APIs

Reason:
Recursive tree responses become inefficient and difficult to paginate at scale.

Consequences:

* Better scalability
* Cleaner frontend navigation model
* Reduced API payload sizes
* Easier caching strategy

Future Reconsideration:
Possible partial-tree loading support later.

---

## Decision 009

Date:
2026-06-08

Title:
Use Temporary Upload Staging Before Final Persistence

Reason:
Direct writes into final storage location increase risk of incomplete/corrupted files during interruptions.

Consequences:

* Improved upload consistency
* Safer upload lifecycle
* Better recovery possibilities
* Reduced partial-write exposure

Future Reconsideration:
May evolve into resumable upload sessions.

---

## Decision 010

Date:
2026-06-08

Title:
Use SHA256 Checksums for Integrity Tracking

Reason:
Storage system requires file integrity validation and future deduplication foundation.

Consequences:

* Corruption detection possible
* Future deduplication foundation established
* Upload integrity verification foundation created

Future Reconsideration:
Potential chunk-level hashing later.

---

## Decision 011

Date:
2026-06-08

Title:
Use Soft Delete Instead of Immediate Hard Delete

Reason:
Immediate permanent deletion is dangerous for user-generated personal storage systems.

Consequences:

* Safer deletion lifecycle
* Trash/recovery system foundation
* Reduced accidental data loss risk
* Physical cleanup deferred to background workflows

Future Reconsideration:
Retention-policy-based cleanup scheduler later.

---

## Decision 012

Date:
2026-07-12

Title:
Use Owned Network Access Instead of Managed Relay Services

Reason:
Remote access should be inspectable and owned end-to-end. A self-managed WireGuard VPN or a self-hosted HTTPS reverse proxy keeps the network path understandable and controlled.

Consequences:

* No dependency on closed relay infrastructure
* Clearer security model
* More setup responsibility for DNS, firewall, keys, and certificates

Future Reconsideration:
Managed relay tools can be reconsidered only if convenience becomes more important than full setup visibility.

---

## Decision 013

Date:
2026-07-12

Title:
Use Mini PC With External SSD and HDD Backup for Production

Reason:
Raspberry Pi pricing is less attractive in 2026, and a used mini PC provides better CPU, RAM, storage, and enclosure value. Live storage will use an external SSD; cheapest backup storage will use an external HDD.

Consequences:

* Better price/performance than a high-end Raspberry Pi kit
* Easier replacement and maintenance
* USB-attached storage is simple to operate
* UPS is recommended to reduce corruption risk during power loss

Future Reconsideration:
Move to NAS-grade hardware if storage, redundancy, or uptime requirements grow.
