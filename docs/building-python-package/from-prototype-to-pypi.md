# From Prototype to PyPI: The Complete Packaging & Distribution Retrospective

## 1. The Starting Point: The Local Prototype

When ContextPortal was conceived, it answered a straightforward question:
> *Can an AI agent retrieve authenticated web pages using the user's existing login session without gaining unrestricted access to their credentials or browser?*

In Phase A and Phase B, we proved the core mechanics:
1. Fast HTTP fetch for public sites.
2. Fallback to Google Chrome via Playwright using a persistent browser profile for login-protected pages.
3. Content extraction via Readability and Markdownify.
4. Model Context Protocol (MCP) server running over STDIO.

### The Prototype Architecture (Fragile & Machine-Coupled)
To run ContextPortal initially, an AI agent required this verbose, brittle configuration:

```json
{
  "mcpServers": {
    "context-portal": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "C:\\Users\\maruthi.n.marella\\ContextPortal\\backend",
        "python",
        "-m",
        "app.mcp.server"
      ]
    }
  }
}
```

#### Why This Failed Developer Adoption:
* **Absolute Path Fragility**: If the project was moved, cloned into a different path, or shared with a colleague, the MCP configuration broke immediately.
* **Virtualenv Entanglement**: Depended on the developer manually managing a Python virtual environment in `backend/`.
* **High Time-To-Value (TTV)**: Required 10+ manual steps before an agent could fetch a single URL.

---

## 2. The Great Packaging Transformation

To make ContextPortal a real tool, we undertook **Phase C: Distribution & Packaging**. 

The goal was radical simplicity:
```bash
uv tool install contextportal
```
Followed by the cleanest possible agent configuration:
```json
{
  "mcpServers": {
    "context-portal": {
      "command": "contextportal",
      "args": ["mcp"]
    }
  }
}
```

Achieving this required solving a series of non-obvious engineering roadblocks.

---

## 3. The 8 Critical Roadblocks & How We Solved Them

### 💥 Roadblock 1: Setuptools Subpackage Omission (`ModuleNotFoundError`)
* **The Problem**: When compiling the initial wheel with `packages = ["app"]`, `setuptools` silently omitted nested subpackages (`app.core`, `app.mcp`). When the installed tool ran, it crashed with `ModuleNotFoundError: No module named 'app.core'`.
* **The Trap**: Using auto-discovery without explicit patterns caused `setuptools` to try to bundle runtime directories (like `playwright_profile/` containing user cookies) into the wheel!
* **The Solution**: Configured explicit recursive subpackage discovery in [`pyproject.toml`](../../backend/pyproject.toml):
  ```toml
  [tool.setuptools.packages.find]
  where = ["."]
  include = ["app", "app.*"]
  ```

---

### 💥 Roadblock 2: Persistent State Directory Fragmentation
* **The Problem**: The prototype stored Chrome profiles in a relative directory `./playwright_profile`. When users ran the CLI from `C:\Users\username\`, sessions saved in `C:\Users\username\playwright_profile`. When the IDE started MCP from another directory, it opened a *different, empty* profile.
* **The Solution**: Centralized persistent state into a deterministic, home-relative directory across all platforms:
  ```python
  from pathlib import Path
  USER_DATA_DIR = Path.home() / ".contextportal" / "playwright_profile"
  ```
  Now, whether invoked via CLI, Cursor, Claude, or Antigravity, the user's authenticated session is shared consistently.

---

### 💥 Roadblock 3: Headless Background Hangs & The `login` CLI
* **The Problem**: When an AI agent runs an MCP server in the background, it runs non-interactively. If the agent hits an authentication wall, launching a headful browser to ask the user to log in can cause the agent host to hang or time out waiting for user interaction.
* **The Solution**: Created the interactive **`contextportal login`** pre-warming command. Developers authenticate their private portals *before* running their agents:
  ```bash
  contextportal login --url https://company.jira.com
  ```
  The browser opens, the user solves SSO/MFA, closes the window, and the session is ready for headless agent use.

---

### 💥 Roadblock 4: Testing Philosophy — "The Stranger Test"
* **The Problem**: Testing within the repository folder masks packaging bugs because Python will happily import local source files (`./app`) even if the installed wheel is completely broken.
* **The Solution**: Established the **Stranger Test** protocol:
  1. Build the wheel: `uv build`.
  2. Install globally: `uv tool install --force .\dist\*.whl`.
  3. Leave the repository entirely: `cd $env:TEMP`.
  4. Execute all verification tests purely from the global binary path (`~/.local/bin/contextportal`).

---

### 💥 Roadblock 5: User-Agent Identity & Responsible Automation (ADR-002)
* **The Problem**: The prototype HTTP client sent generic `python-httpx/0.28.1`. While functional, it reflected an implementation library rather than the application, and looked like an unbranded scraper to web operators.
* **The Solution**: Codified [ADR-002](../../decisions/ADR-002-http-client-identity-and-user-agent.md), establishing transparent application identification:
  ```text
  User-Agent: ContextPortal/0.1.0 (+https://github.com/NavadeepDj/ContextPortal)
  ```
  - **Tier 1 (HTTP)** identifies honestly with the repository URL as a visitor badge.
  - **Tier 2 (Browser)** legitimately uses Chrome's native header because it executes via real Google Chrome on the host machine.

---

### 💥 Roadblock 6: Windows File Locking (`os error 32` & `os error 5`)
* **The Problem**: During re-installation (`uv tool install --force`), Windows threw `Access is denied (os error 5)` and `os error 32`.
* **The Root Cause**: Antigravity IDE was actively connected to `contextportal` over STDIO in the background. On Windows, a running executable places a mandatory file-lock on its binary and locks its parent directory (`...\Scripts`) from deletion.
* **The Solution**: Terminate active background processes prior to re-installation:
  ```powershell
  Get-Process | Where-Object { $_.Path -like "*contextportal*" } | Stop-Process -Force
  ```

---

### 💥 Roadblock 7: Corporate TLS Handshake Resets on Reserved Domains
* **The Problem**: Testing `contextportal fetch https://example.com` failed with:
  ```text
  httpcore.ConnectError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol
  ```
* **The Root Cause**: Corporate security gateways (e.g. Zscaler, Palo Alto) often drop or terminate TLS handshakes on RFC-reserved documentation domains (`example.com`) on port 443.
* **The Solution**: Tested across production domains (`httpbin.org`, `github.com`, `joinhandshake.com`), confirming that HTTPS and our User-Agent work flawlessly.

---

### 💥 Roadblock 8: TestPyPI Split-Index Resolution
* **The Problem**: TestPyPI only hosts test uploads; it does not host the thousands of public dependencies (`playwright`, `fastapi`, `pydantic`). Installing from TestPyPI alone fails with `No matching distribution found`.
* **The Solution**: Configured multi-index resolution:
  ```powershell
  uv tool install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ contextportal
  ```
  `uv` fetches `contextportal` from TestPyPI and resolves all dependencies from main PyPI.

---

## 4. The Product Evolution Timeline

```text
[Phase A & B] Prototype
  │  • uv run python -m app.mcp.server
  │  • Fragile JSON configs with absolute paths
  │  • Relative ./playwright_profile
  │
  ▼
[Phase C.1] Local Package
  │  • pyproject.toml with [project.scripts]
  │  • Setuptools subpackage discovery
  │  • ~/.contextportal/playwright_profile deterministic state
  │
  ▼
[Phase C.2] The Stranger Test Gauntlet
  │  • Level 1: Local Source Install (Verified in $env:TEMP)
  │  • Level 2: Wheel Compilation & Distribution Audit
  │  • Level 3: Autonomous AI Agent E2E Validation
  │
  ▼
[Housekeeping] Professional Polish
  │  • ADR-002 ContextPortal/0.1.0 User-Agent
  │  • OpenWiki automated CI workflow
  │  • Professional README & MIT LICENSE
  │
  ▼
[Release 0.1] Registry Distribution
     • Official package name "contextportal" registered
     • Published to TestPyPI
     • Live installation and dual-tier retrieval from $env:TEMP
```

---

## 5. Summary & Key Takeaways

1. **Packaging is UX**: Packaging isn't just build scripts; it defines how fast a user can experience value.
2. **Context, Not Control**: Security is maintained at every step—no cookies or tokens leave the local machine.
3. **Registry Verified**: `contextportal` is now ready for production release to PyPI and automated OIDC Trusted Publishing.

