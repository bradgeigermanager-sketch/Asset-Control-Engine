# Architecture Overview
- Ingest connectors -> Normalization -> Canonical store -> Matching engine -> Resolution layer -> Audit anchoring
- Backend: FastAPI prototype. Replace in-memory stores with Postgres JSONB.
- Frontend: React + TypeScript operator UI.
- Audit: append-only JSONL with payload hashes; anchor externally in production.
