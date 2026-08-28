# Implementation Plan

Aligned with the core thesis in `PRODUCT_THESIS.md`.

## Current Objective: Phase A — Retrieval Proof (Local MVP)

**Goal:** Prove the core product abstraction: `URL → ContextPortal → Clean Markdown`.
The agent requests a URL, and ContextPortal retrieves it using either a normal HTTP fetch (if public) or a legitimate authorized browser session (if protected).

### Phase A: Thin Local MVP
We will build a minimal, local-only Python implementation that demonstrates the end-to-end flow.

#### Step 1: Core Dependencies
- Add `playwright` for browser automation (the authorized retrieval mechanism).
- Add `httpx` (already present) for normal public fetching.
- Add `readability-lxml` and `markdownify` for content extraction and normalization.

#### Step 2: The Retrieval Engine
Create `backend/app/core/retriever.py`:
- **`fetch_public(url)`**: Attempts a standard HTTP GET. If it returns 200 and looks like public content, it returns it. If it hits 401/403/auth walls, it fails over to the authenticated path.
- **`fetch_authenticated(url)`**: Launches a visible Playwright browser using a persistent context.
  - Navigates to the URL.
  - Pauses to allow the user to manually log in if they aren't already.
  - Once the target content is loaded, extracts the DOM.
- **`extract_markdown(html)`**: Cleans the HTML (strips scripts/styles/nav), identifies primary content, and converts it to markdown.

#### Step 3: The Agent Interface
Create a simple local FastAPI endpoint (`GET /c?url=<URL>`) or a CLI command (`python -m contextportal fetch <URL>`).
- This acts as the boundary. The agent only interacts with this interface, never the browser directly.

#### Next Steps (Deferred until Phase A is proven)
- Phase B: Agent Interface (MCP server).
- Phase C: Resource Isolation (Strict boundaries).
- Phase D: Authentication Session Management (Redis).
- Phase E: Security Hardening (SSRF, origin checks).
- Phase F: Production Infrastructure.