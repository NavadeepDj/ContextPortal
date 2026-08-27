---
type: architecture decision map
title: Decisions and Implementation Status
description: Source-of-truth hierarchy and evidence-backed status matrix for ContextPortal's current implementation versus planned architecture.
tags: [architecture, adr, implementation-status]
---

# Decisions and Implementation Status

ContextPortal has more architecture intent than runtime implementation today. Use this page to avoid confusing product plans with implemented code.

## Source-of-truth hierarchy

1. **Current source code and tests** define what is actually implemented.
2. **`decisions/` ADRs** define accepted architecture decisions. `ADR-001` currently changes the infrastructure direction away from PostgreSQL and toward ephemeral Redis state.
3. **`AGENT_RULES.md`** defines required engineering and security behavior for coding agents.
4. **`PROJECT_SPEC.md`** defines product identity, MVP goals, security requirements, and target user flow.
5. **`IMPLEMENTATION_PLAN.md`** defines a phased roadmap. Some early plan text still mentions PostgreSQL, but ADR-001 supersedes that for current architecture.

Do not reinterpret these documents in code or docs. If code and docs disagree, document the discrepancy and prefer current code for implementation status while preserving ADR decisions.

## Accepted ADR

`decisions/ADR-001-ephemeral-context.md` accepts an ephemeral context proxy architecture:

- private content must not be stored permanently;
- PostgreSQL is deferred;
- Redis owns temporary state such as auth sessions, context tokens, expiration, revocation, and rate limiting;
- context delivery should eventually use live fetch plus a short Redis cache.

This decision is why the current `docker-compose.yml` contains Redis only.

## Implemented versus planned matrix

| Area | Current implementation | Evidence | Status |
| --- | --- | --- | --- |
| Backend process | FastAPI app with title from settings | `backend/app/main.py` | Implemented bootstrap |
| Backend API | `GET /health` only | `backend/app/main.py` | Implemented |
| Redis connectivity | Module-level async Redis client and `PING` check | `backend/app/redis.py` | Implemented bootstrap |
| Configuration | `APP_NAME`, `REDIS_URL` via Pydantic settings | `backend/app/config.py`, `.env.example` | Implemented bootstrap |
| Frontend | Create-next-app template page and root layout | `frontend/src/app/page.tsx`, `layout.tsx` | Implemented scaffold only |
| Local infrastructure | Redis 7 Alpine compose service | `docker-compose.yml` | Implemented bootstrap |
| PostgreSQL | No service, models, migrations, or dependency | ADR-001 and repository inventory | Deferred by ADR |
| Auth sessions | No manager or API | repository inventory | Planned |
| Source connectors | No interface or connector implementation | repository inventory | Planned |
| Browser automation | No Playwright dependency or code | manifests and repository inventory | Planned |
| SSRF protection | No URL-fetching path and no validator yet | repository inventory | Required before arbitrary fetch |
| Context tokens | No generation, hashing, validation, expiration, or revocation code | repository inventory | Planned |
| Agent endpoint | No `GET /c/{token}` route | `backend/app/main.py` | Planned |
| Content extraction | No extraction or Markdown normalization code | repository inventory | Planned |
| Backend tests | One health test, currently contains `ASITransport` typo | `backend/tests/test_health.py` | Present but failing until fixed |
| Product CI | No code validation workflow; only OpenWiki update workflow exists | `.github/workflows/openwiki-update.yml` | Not implemented |

## Git history signal

The current Git history contains one relevant commit, `4d0cab6 feat: complete Phase 0 repository bootstrap and Ephemeral proxy ADR`. That supports treating this repository as a Phase 0 bootstrap rather than an MVP-complete product.

## How to continue safely

Before adding any protected URL retrieval, implement and test the security foundations from `AGENT_RULES.md`: URL validation, SSRF protections, isolated sessions, high-entropy token handling, expiration, revocation, and secret-safe logging. The details are summarized in [Security Boundaries](../security/implemented-boundaries.md), and the likely next implementation areas are mapped in [Implementation Status](../roadmap/implementation-status.md).