# ContextPortal Product & Release Roadmap

## 🎯 The North Star Principle
> **"One install. One setup. One MCP server. Zero credential handling."**

The goal of ContextPortal is not just to be a Python package, but to minimize the Time-To-Value (TTV) for an AI user. A developer should go from hearing about ContextPortal to having an AI agent fetch an authenticated webpage in under 2 minutes.

No API keys. No cloud accounts. No copying cookies. No manual MCP JSON configuration.

---

## 🚀 Release 0.1 — Developer Preview
**Status:** Completed ✅

The transition from "my local project" to "public developer tool".
- [x] Functional CLI (`login`, `fetch`, `mcp`)
- [x] Packaged as a standard Python wheel
- [x] Published to TestPyPI for validation
- [x] Published to PyPI (`uv tool install contextportal`)

**Target Audience**: Developers and early adopters.

---

## 🪄 Release 0.2 — "It Just Works" (The UX Update)
**Status:** Implemented & Verified ✅

Transforming the installation experience from 5 minutes to 30 seconds by hiding the complexity of JSON, virtual environments, and browser profiles.

- [x] **`contextportal setup`**: Auto-detects installed AI clients (Claude Desktop, Cursor, Antigravity) and safely injects the `context-portal` MCP server with atomic backups.
- [x] **`contextportal doctor` / `status`**: Diagnostics command to audit Python environment, PATH accessibility, browser profile, and client readiness.
- [x] Comprehensive test suite for client discovery, atomic updates, and idempotency.

---

## 🧠 Release 0.3 — Intelligent Retrieval
**Status:** Planned (Formerly Phase D)

Upgrading the retrieval engine from a simple fallback to a 4-tier intelligent router:
1. **Tier 0 (HTTP)**: Blazing fast for static sites.
2. **Tier 1 (Headless JS)**: Renders React/Vue/Angular SPAs without launching a visible browser.
3. **Tier 2 (Persistent Browser)**: Transparently uses the saved session for auth-walled content.
4. **Tier 3 (Interactive Login)**: Prompts the user when a session is missing or expired.

---

## 📦 Release 0.4 — Binary Distribution
**Status:** Planned

Solving the "I don't want Python" problem.
- Standalone executables: `ContextPortal-Setup.exe`, `ContextPortal.dmg`, `ContextPortal.AppImage`.
- Python disappears entirely from the user's mental model.

---

## 🌐 Release 1.0 — Universal Agent Gateway
**Status:** Planned

The mature architecture where ContextPortal serves as the standard, secure, local bridge between any AI agent and the user's authenticated web identity.

