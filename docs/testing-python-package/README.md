# Testing the ContextPortal Python Package

## 1. The "Stranger Test" Philosophy

Testing an internal codebase in-place (`cd backend && python ...`) often conceals fundamental deployment bugs (hardcoded paths, missing dependencies, unexported submodules).

To validate **Phase C (Distribution & Developer Experience)**, we execute the **Stranger Test**:
> *Can an external developer install ContextPortal, run it from a completely random directory, authenticate to a private resource, and feed clean context to an AI agent without knowing anything about our repository structure?*

---

## 2. Test Matrix & Validation Results

| Test # | Objective | Command | Result | Notes |
|---|---|---|---|---|
| **Test 1** | Standalone Global Installation | `uv tool install --force ./backend` | ✅ **PASS** | Installed executable into `~/.local/bin/contextportal` |
| **Test 2** | CLI Subcommand Discovery | `contextportal --help` | ✅ **PASS** | Successfully registered `mcp`, `login`, and `fetch` |
| **Test 3** | Public Content Retrieval | `contextportal fetch https://example.com` | ✅ **PASS** | Executed outside repo. Returned clean markdown via HTTP |
| **Test 4** | Session Pre-warming | `contextportal login` | ✅ **PASS** | Opens persistent Chrome window with zero cookie copying |
| **Test 5** | Protected Content Retrieval | `contextportal fetch <protected_url>` | ✅ **PASS** | Successfully reads from global `~/.contextportal/playwright_profile` |
| **Test 6** | MCP Server Launch | `contextportal mcp` | ✅ **PASS** | Operates over STDIO transport |

---

## 3. Difficulties Encountered & Root Cause Analysis

During our live gauntlet of "Stranger Tests", we diagnosed and resolved three critical bugs:

### Bug 1: `ModuleNotFoundError: No module named 'app.core'`
- **Symptom**: `contextportal fetch` crashed immediately on external execution.
- **Root Cause**: `pyproject.toml` used a static `packages = ["app"]` directive which omitted all nested submodules (`app/core`, `app/mcp`).
- **Resolution**: Replaced with `[tool.setuptools.packages.find]` using `include = ["app", "app.*"]`.

### Bug 2: Fragmented Profile State via Relative Paths
- **Symptom**: Running `contextportal login` in folder A did not make the session available to `contextportal mcp` started in folder B.
- **Root Cause**: Retriever and CLI referenced `./playwright_profile`, which resolved relative to the user's active `CWD`.
- **Resolution**: Updated `retriever.py` and `cli.py` to use a deterministic user-scoped path: `Path.home() / ".contextportal" / "playwright_profile"`.

### Bug 3: Background Non-Interactive Browser Authentication
- **Symptom**: Running `contextportal fetch` against a protected page inside a background process timed out after 5 minutes (`RuntimeError: Authentication timed out`).
- **Root Cause**: Background worker processes cannot display an interactive Chrome GUI for human captcha/SSO solving.
- **Resolution**: Built the explicit `contextportal login` workflow so users can pre-warm authentication interactively before triggering automated agent workflows.

---

## 4. Manual Testing Runbook (Step-by-Step)

Here are the exact commands to independently verify ContextPortal from start to finish:

### Step 1: Install Globally
```powershell
# From the ContextPortal repository root
uv tool install --force ./backend
```

### Step 2: Ensure CLI is on PATH
If `contextportal` is not immediately found in your terminal:
```powershell
$env:PATH = "C:\Users\$env:USERNAME\.local\bin;$env:PATH"
```
Verify the installation:
```powershell
contextportal --help
```

### Step 3: Test Public Fetch (From any directory)
Open an empty directory (e.g. `C:\Users\<user>\Documents`) and run:
```powershell
contextportal fetch https://example.com
```
*Expected output: Returns Example Domain Markdown via HTTP.*

### Step 4: Pre-warm Your Authenticated Session
Run the login command in a visible interactive terminal:
```powershell
contextportal login --url https://project-dynamo.learn.joinhandshake.com/introduction
```
1. A Chrome browser window will open.
2. Sign in to your account.
3. Once logged in, simply close the browser window.
4. Your session is now saved to `~/.contextportal/playwright_profile`.

### Step 5: Test Authenticated Fetch
In the same terminal or any other folder, fetch the protected URL:
```powershell
contextportal fetch https://project-dynamo.learn.joinhandshake.com/introduction
```
*Expected output: ContextPortal detects the active session, navigates directly to the target content without prompting for login, and outputs clean Markdown with `Retrieval Method: browser (Authenticated: True)`.*

### Step 6: Test MCP STDIO Server
Test that the MCP server initializes over standard input/output:
```powershell
contextportal mcp
```
*(Press `Ctrl+C` to exit).*

---

## 5. Detailed Test Reports

- 📄 **[Level 1: Local Source Install Test Report](local-test/README.md)**
- 📄 **[Level 2: Distributable Wheel (.whl) Test Report](wheel-test/README.md)**


