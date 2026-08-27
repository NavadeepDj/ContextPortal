---
type: "Reference"
title: "OpenWiki Skeleton for ContextPortal"
openwiki_generated: true
---

# OpenWiki Skeleton for ContextPortal

## Inventory and evidence brief

### Repository scope and source-of-truth documents
- `PROJECT_SPEC.md` defines the product vision, MVP boundaries, security requirements, connector concept, and planned long-term architecture.
- `AGENT_RULES.md` defines required engineering behavior, especially security-first development, session isolation, SSRF protection, token rules, and definition of done.
- `IMPLEMENTATION_PLAN.md` defines the phased roadmap. Current code only implements a small Phase 0 bootstrap subset.
- `decisions/ADR-001-ephemeral-context.md` supersedes earlier PostgreSQL-oriented planning by accepting an ephemeral proxy architecture: no persistent content storage, no PostgreSQL for now, Redis for temporary state, and hybrid live-fetch plus short Redis cache delivery.
- Git history currently has one relevant commit: `4d0cab6 feat: complete Phase 0 repository bootstrap and Ephemeral proxy ADR`, which supports that the repository is at bootstrap stage.

### Manifest-backed components
1. Backend service (`backend/pyproject.toml`)
   - Runtime: Python 3.12 FastAPI app in `backend/app/main.py`.
   - Dependencies: `fastapi`, `uvicorn[standard]`, `redis[hiredis]`, `pydantic-settings`, `httpx`.
   - Dev tools: `pytest`, `pytest-asyncio`, `pytest-cov`, `ruff`, `mypy`.
   - Entrypoint: `uvicorn app.main:app --reload`.
   - Implemented API: `GET /health` only.
   - Redis ownership: `backend/app/redis.py` creates a module-level async Redis client from `settings.redis_url` and exposes `check_redis_connection()`.
   - Configuration: `backend/app/config.py` loads `APP_NAME` and `REDIS_URL` defaults via Pydantic settings and optional `.env`.
   - Tests: `backend/tests/test_health.py` attempts an async ASGI health endpoint test but currently imports `ASGITransport` and then calls misspelled `ASITransport`, so the test suite is expected to fail until corrected.
2. Frontend application (`frontend/package.json`)
   - Runtime: Next.js 16 App Router, React 19, TypeScript.
   - Entrypoint scripts: `pnpm dev`, `pnpm build`, `pnpm start`, `pnpm lint`.
   - Current UI: unmodified create-next-app home page in `frontend/src/app/page.tsx`, layout metadata says `Create Next App`, global Tailwind CSS variables in `globals.css`.
   - Implemented product flow: none yet. No URL input, authentication, processing, or context-ready screens are implemented.
3. Infrastructure (`docker-compose.yml`, `.env.example`, `.github/workflows/openwiki-update.yml`)
   - Docker Compose currently runs Redis 7 Alpine only with append-only persistence and port `6379:6379`.
   - `.env.example` contains placeholder/non-secret `APP_NAME` and `REDIS_URL`.
   - No PostgreSQL service is present, consistent with ADR-001 rather than the older implementation-plan phases.
   - GitHub Actions workflow only updates OpenWiki documentation and does not run product CI checks.

### Runtime importance ranking
1. Architecture and security decisions: highest importance because they constrain all future implementation and prevent contradictions between code and roadmap.
2. Backend bootstrap: highest implemented runtime centrality; owns the only API and Redis connectivity.
3. Redis ephemeral-state infrastructure: central future state mechanism and only external runtime service currently configured.
4. Frontend bootstrap: visible user-facing application but currently template-only.
5. Development/testing workflow: important because current focused backend test has a defect, and CI is documentation-only.
6. Planned connectors/auth/browser/content/context flows: high product importance but mostly unimplemented; document as roadmap/status, not code reality.

### Substantial APIs and workflows to cover
- Implemented health-check request flow: `GET /health` -> FastAPI -> `check_redis_connection()` -> Redis `PING` -> JSON status.
- Implemented configuration flow: environment/default settings -> `settings` singleton -> FastAPI title and Redis URL.
- Implemented local infrastructure flow: `docker compose up -d` starts Redis; backend reads Redis URL; frontend starts independently.
- Architectural future flow from docs/ADR: authenticated resource -> legitimate user auth -> connector/browser retrieval -> extraction/normalization -> ephemeral Redis context token/cache -> agent URL. Must be marked planned unless code implements it.
- Current absence boundaries: no SourceConnector interface, no authentication/session manager, no Playwright/browser automation, no content extraction, no context token endpoint, no revocation API, no PostgreSQL/migrations.

## Planned wiki files

### `/openwiki/architecture/overview.md`
Document the repository's current system architecture and implementation status. Include an implemented-component diagram showing frontend, backend, Redis, docs/ADR inputs, and the only implemented `/health` flow. Clearly distinguish current code from planned product architecture and explain why ADR-001 makes ContextPortal an ephemeral proxy rather than a persistent private-data warehouse.

### `/openwiki/architecture/decisions-and-status.md`
Document source-of-truth documents and the accepted ADR. Explain precedence between PROJECT_SPEC, AGENT_RULES, IMPLEMENTATION_PLAN, ADR-001, and code. Include a concise implemented-vs-planned matrix covering backend, frontend, Redis, PostgreSQL, auth sessions, connectors, browser automation, context tokens, content extraction, agent endpoint, tests, and CI.

### `/openwiki/backend/service.md`
Dedicated backend service page. Cover FastAPI app composition, `GET /health`, settings, Redis helper, dependencies, current API surface, error/failure behavior, narrow tests, validation commands, and known test typo. Include a sequence diagram for health check.

### `/openwiki/backend/configuration.md`
Document backend configuration ownership: `Settings`, environment variable names, `.env.example` placeholders, default values, local `.env` behavior, and safe handling of secrets. Explain that only `APP_NAME` and `REDIS_URL` are currently implemented settings.

### `/openwiki/frontend/app.md`
Dedicated frontend application page. Cover Next.js App Router structure, current create-next-app UI, root layout, metadata, Tailwind/global CSS, scripts, dependencies, product-flow gap, and validation. Make clear that no ContextPortal-specific frontend workflow is implemented yet.

### `/openwiki/infrastructure/local-runtime.md`
Document Docker Compose Redis service, port mapping, append-only command, local startup order from README, no PostgreSQL, no production Dockerfiles, and the OpenWiki-only GitHub Actions workflow. Include focused validation commands and state what infrastructure exists versus planned.

### `/openwiki/security/implemented-boundaries.md`
Document implemented and unimplemented security boundaries. Ground implemented claims in code: no protected URL fetching exists, no credentials are collected by UI, no persistent content storage service exists, Redis is the only configured state service. Ground required future constraints in AGENT_RULES/PROJECT_SPEC/ADR-001: SSRF, session isolation, tokens, revocation, no secrets in logs, prompt-injection separation. Include a safety checklist for future changes.

### `/openwiki/workflows/development-and-testing.md`
Document setup, run, lint/type/test commands for backend and frontend from manifests and README. Cover test ownership, the current `test_health.py` ASGITransport typo, expected validation posture, and the fact that GitHub Actions currently updates docs rather than validating product code.

### `/openwiki/roadmap/implementation-status.md`
Document where development should continue using IMPLEMENTATION_PLAN and ADR-001 without implying implementation. Map phases to current code reality, emphasizing Phase 0 partial bootstrap, ADR-driven removal/deferment of PostgreSQL, next likely code areas, and evidence-backed backlog items.

### `/openwiki/quickstart.md`
Write last. Entry point with high-level map, links to all major concept pages, quick task-routing table, current status summary, safe development rules, focused validation commands, and backlog/deferrals with source anchors and reasons.
