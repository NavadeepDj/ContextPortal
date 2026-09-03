# ContextPortal Product & Release Roadmap

## 🎯 The North Star Principle
> **"One install. One setup. One MCP server. Zero credential handling."**

The goal of ContextPortal is not just to be a Python package, but to minimize the Time-To-Value (TTV) for an AI user. A developer should go from hearing about ContextPortal to having an AI agent fetch an authenticated webpage in under 2 minutes.

No API keys. No cloud accounts. No copying cookies. No manual MCP JSON configuration.

---

## 🚀 Release 0.1 — Developer Preview (CURRENT FOCUS)
**Status:** In Progress

The transition from "my local project" to "public developer tool".
- [x] Functional CLI (`login`, `fetch`, `mcp`)
- [x] Packaged as a standard Python wheel
- [ ] Published to TestPyPI for validation
- [ ] Published to PyPI (`uv tool install contextportal`)

**Target Audience**: Developers and early adopters who understand how to configure MCP manually.

---

## 🪄 Release 0.2 — "It Just Works" (The UX Update)
**Status:** Planned

Transforming the installation experience from 5 minutes to 30 seconds by hiding the complexity of JSON, virtual environments, and browser profiles.

- **`contextportal setup`**: A unified command that handles:
  - Browser profile initialization
  - Chrome detection
  - Interactive login sequence
  - Session validation
- **MCP Auto-Configuration**: `setup` detects installed AI clients (Cursor, Claude Desktop, Antigravity, VS Code) and automatically injects the `contextportal mcp` connection into their configurations.
- **`contextportal status`**: A diagnostic command to check installation, browser connection, and MCP readiness.

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

