# Asset-Control-Engine
# Asset Control Engine Prototype

## Overview
Prototype reconciliation engine with FastAPI backend and React + TypeScript UI. Includes seed data generator, basic matcher, audit store, and CI test scaffold.

## Quickstart (local)
1. Build and run services:
   docker-compose -f infra/docker-compose.yml up --build
2. Generate seeds:
   python data/generate_seeds.py
3. API docs:
   http://localhost:8000/docs
4. UI:
   http://localhost:3000

## Notes
- This scaffold uses in-memory stores for quick prototyping. Replace with Postgres and S3 for production.
- Configure OAuth2 and MFA before enabling high-risk endpoints.
