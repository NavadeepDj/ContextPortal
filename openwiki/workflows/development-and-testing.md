---
type: development workflow
title: Development and Testing Workflows
description: Local setup, validation commands, current test coverage, and workflow gaps for ContextPortal developers and coding agents.
tags: [development, testing, validation]
---

# Development and Testing Workflows

ContextPortal is at bootstrap stage, so the main developer workflow is starting Redis, running the backend health API, and running the scaffolded frontend. Product-level security and end-to-end tests are not implemented yet.

## Local setup

From the repository root:

```bash
docker compose up -d
```

Backend:

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
pnpm install
pnpm dev
```

## Backend validation

`backend/pyproject.toml` configures pytest, Ruff, and mypy. Runtime dependencies cover FastAPI serving and Redis access (`fastapi`, `uvicorn[standard]`, `redis[hiredis]`, `pydantic-settings`, `httpx`); dev dependencies cover async tests and quality gates (`pytest`, `pytest-asyncio`, `pytest-cov`, `ruff`, `mypy`). Pytest is configured with `asyncio_mode = "auto"` and `testpaths = ["tests"]`, so async tests under `backend/tests` are discovered without per-test event-loop setup. Ruff targets Python 3.12, line length 88, and rule families `E`, `F`, `I`, `N`, `W`, and `UP`; the `F` family is the static check that would flag undefined names such as the current transport typo. Mypy is configured for Python 3.12 with `strict = true`.

Use:

```bash
cd backend
uv run pytest
uv run ruff check .
uv run mypy app
```

Current caveat: `backend/tests/test_health.py` imports `ASGITransport` but calls `ASITransport`, a symbol that is neither imported nor defined. That typo should be fixed before treating the backend test suite as passing. The intended behavior of the test is to assert that `GET /health` returns HTTP 200 and JSON `status: ok` even when Redis is not running.

## Frontend validation

`frontend/package.json` exposes:

```bash
cd frontend
pnpm lint
pnpm build
```

There are no frontend tests yet. When ContextPortal-specific UI is added, tests should cover form validation, backend interaction, loading/error states, and safe display of generated context URLs.

## Documentation automation & OpenWiki
 
 The repository uses **OpenWiki** to generate and maintain a living codebase map under `openwiki/`.
 
 ### Updating Documentation
 After making code or schema changes, update the wiki incrementally:
 ```bash
 openwiki --update
 ```
 
 ### Provider & Model Configuration
 - **Gemini / Google AI Studio**:
   ```powershell
   $env:OPENWIKI_PROVIDER="gemini"
   $env:GEMINI_API_KEY="your-api-key"
   openwiki --update --modelId gemini-2.5-flash
   ```
 - **OpenAI**:
   ```powershell
   $env:OPENWIKI_PROVIDER="openai"
   $env:OPENAI_API_KEY="your-api-key"
   openwiki --update
   ```
 
 ### Rate Limit Handling
 If you encounter a `429 Quota Exceeded` (e.g. Free Tier TPM limits), wait 30–60 seconds for the rolling rate-limit window to clear and re-run `openwiki --update`. OpenWiki preserves all completed pages and continues incrementally.
 
 The repository also includes `.github/workflows/openwiki-update.yml` which updates OpenWiki documentation on a schedule or manual dispatch and opens a pull request. It is not a substitute for product CI.
 
 ## Recommended validation by change area
 
 | Change area | Focused checks | Notes |
 | --- | --- | --- |
 | Backend health/config/Redis | `uv run pytest`, `uv run ruff check .`, `uv run mypy app` | Start Redis if manually verifying the connected branch. |
 | Frontend scaffold/UI | `pnpm lint`, `pnpm build` | Add component or integration tests when product UI appears. |
 | Docker Compose | `docker compose up -d`, `docker compose ps`, backend `/health` | Current compose only manages Redis. |
 | Security-sensitive URL/session/token code | Add negative tests before implementation is declared complete | Required by `AGENT_RULES.md`; no such code exists yet. |
 | Documentation | OpenWiki validation through generated workflow or local OpenWiki command | Keep claims source-grounded and distinguish planned work. |

## Agent workflow rules

`AGENT_RULES.md` requires agents to inspect the repository, plan the smallest secure change, identify or write tests, run relevant checks, and avoid declaring completion without executed validation. For ContextPortal, never implement protected retrieval before SSRF, session isolation, token, and logging boundaries have tests.