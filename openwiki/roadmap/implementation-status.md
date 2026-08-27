---
type: implementation roadmap
title: Implementation Status and Next Development Areas
description: Evidence-backed map from the ContextPortal implementation plan and ADR-001 to what is currently implemented and where development should continue.
tags: [roadmap, implementation-status, planning]
---

# Implementation Status and Next Development Areas

This page maps `IMPLEMENTATION_PLAN.md` to current code reality. It is not a product commitment; it is a navigation aid for engineers and agents deciding where to work next.

## Current phase assessment

The repository matches an early Phase 0 bootstrap:

- FastAPI backend exists.
- Next.js frontend exists.
- Redis local infrastructure exists.
- `.env.example` exists with non-secret placeholders.
- Basic tooling is declared in manifests.
- A backend health endpoint exists.

The repository is not MVP-complete and does not implement the protected Handshake flow described in `PROJECT_SPEC.md`.

## ADR-driven roadmap adjustment

`IMPLEMENTATION_PLAN.md` originally includes PostgreSQL as a Phase 0 and Phase 2 concern. `decisions/ADR-001-ephemeral-context.md` supersedes that direction by deciding:

- no persistent private content storage;
- no PostgreSQL unless a future requirement justifies it;
- Redis for temporary state;
- hybrid live fetch plus short cache delivery.

Therefore, next work should not add PostgreSQL merely because the older plan mentions it. If persistence becomes necessary, write a new ADR or update the existing decision first.

## Status by implementation-plan area

| Plan area | Current status | Next evidence-backed work |
| --- | --- | --- |
| Phase 0 repository bootstrap | Partially implemented | Fix backend health test typo; verify backend/frontend tooling; consider product CI. |
| Phase 1 architecture boundaries | Not implemented as packages | Create explicit modules only when code needs them: `api`, `auth`, `connectors`, `contexts`, `security`, `storage` or ADR-aligned equivalents. |
| Phase 2 database | Deferred | Do not add PostgreSQL under current ADR. Model temporary state in Redis when implementing sessions/tokens. |
| Phase 3 security foundation | Not implemented | Add URL validation, SSRF protections, token primitives, and tests before network retrieval. |
| Phase 4 auth session infrastructure | Not implemented | Design isolated session lifecycle and Redis TTL ownership before connector work. |
| Phase 5 authenticated web connector | Not implemented | Add connector interface and Playwright/browser automation only after security/session foundations. |
| Phase 6 Handshake MVP | Not implemented | Implement only legitimate authentication and authorized retrieval; no password collection or CAPTCHA bypass. |
| Phase 7 content extraction | Not implemented | Build extraction/Markdown normalization after retrieval path exists. |
| Phase 8 context engine | Not implemented | Implement ephemeral context representation aligned with Redis TTL/cache model. |
| Phase 9 secure context URLs | Not implemented | Generate high-entropy bearer tokens, store hashes where possible, enforce expiration and revocation. |
| Phase 10 agent retrieval endpoint | Not implemented | Add `GET /c/{token}` only after token validation and context retrieval exist. |
| Phase 11 frontend MVP | Not implemented | Replace template UI with protected URL input and flow screens once backend APIs exist. |
| Phase 12 onward | Not implemented | E2E, security review, observability, production containers, CI/CD, MCP, and extra connectors remain future work. |

## Suggested immediate backlog

1. **Fix the health test typo**: `backend/tests/test_health.py` should use `ASGITransport`, matching the import. Reason: the only focused backend test is currently broken.
2. **Add product CI**: create a workflow that runs backend tests/lint/type checks and frontend lint/build. Reason: current GitHub Actions only updates OpenWiki.
3. **Clarify readiness versus liveness**: decide whether Redis disconnection should be a readiness failure while `/health` remains liveness. Reason: `PROJECT_SPEC.md` mentions `/health` and `/ready`; only `/health` exists.
4. **Implement security foundations before fetch**: URL validation and SSRF tests should precede any endpoint accepting user URLs. Reason: required by `AGENT_RULES.md` and product security requirements.
5. **Design Redis key ownership and TTLs**: future auth sessions, revocations, token hashes, and short content cache all need namespacing and lifecycle rules. Reason: ADR-001 assigns ephemeral state to Redis.

## What not to build yet without explicit request

Do not add Slack, GitHub, Jira, Notion, vector databases, embeddings, RAG, MCP, billing, team collaboration, or autonomous agents as part of bootstrap work. `PROJECT_SPEC.md` and `IMPLEMENTATION_PLAN.md` both treat these as future or out-of-MVP capabilities.