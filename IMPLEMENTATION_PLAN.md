# Implementation Plan

Aligned with the core thesis in `PRODUCT_THESIS.md`.

## Current Objective: Phase C — Distribution & Developer Experience

**Goal:** Transform ContextPortal from a local prototype into an easily installable, agent-agnostic developer tool with a seamless "First 5 Minutes" UX. 
The developer should never have to manually write absolute paths in MCP configurations or fiddle with browser cookies.

### Phase A: Retrieval Proof (Local MVP) — ✅ COMPLETED
- `playwright` for persistent browser sessions.
- `httpx` for lightweight HTTP fallback.
- Readability + Markdownify extraction pipeline.
- End-to-end extraction from a protected enterprise resource proven.

### Phase B: Agent Interface (MCP) — ✅ COMPLETED
- Expose the retrieval capability (`fetch_context`) through the Model Context Protocol (STDIO transport).
- SSRF and credential-leakage hardening.
- Live validation with real AI agents on 10 edge-case URLs (Phase B.6).

### Phase C: Distribution & Developer Experience (CURRENT)

#### C.1 — Package ContextPortal
Turn the backend into a proper installable Python package via `pyproject.toml` `[project.scripts]`.
**Expected Outcome:** Developer can run `uv tool install contextportal` (or `pip install`) and immediately have the `contextportal` CLI available globally.

#### C.2 — Trivial MCP Configuration
Replace fragile, absolute-path JSON configurations with simple command execution.
**Expected Outcome:** MCP configuration becomes as simple as `{"command": "contextportal", "args": ["mcp"]}`.

#### C.3 — Seamless Auth/Session Setup (`contextportal login`)
Provide a dedicated CLI command for developers to easily pre-warm their authenticated sessions. We should never ask developers to copy/paste cookies or authentication tokens.
**Expected Outcome:** Running `contextportal login` opens the persistent browser. The developer logs in normally, closes the window, and the session is permanently ready for the AI agent to use in the background.

#### C.4 — Agent-Agnostic Validation
Ensure ContextPortal works identically and frictionlessly across Claude Desktop, Cursor, and Antigravity.

#### C.5 — The "First 5 Minutes" UX Redesign
Rewrite the `README.md` to immediately communicate the value prop ("The authenticated fetch layer for AI agents") and provide a 3-step quickstart.

### Future Roadmap
- **Phase D:** Intelligent Retrieval Routing (Levels 0-3: Caching, Fast HTTP, Headless JS, Persistent Auth).
- **Phase E:** Remote MCP & Cloud Deployment (Multi-tenant public retrieval with Local Gateway hybrid).