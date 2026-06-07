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
- Faster development
- Easier debugging
- Simpler deployment
- Easier transactions

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
- Easier implementation
- Faster iteration
- Simpler debugging

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
- Rapid development
- Strong typing with Pydantic
- Easy API documentation