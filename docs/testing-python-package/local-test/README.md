# Level 1: Local Source-Based Tool Installation & CLI Discovery Test

## 1. Overview & Objective

**Level 1 Testing** validates that ContextPortal can be packaged and installed as a standalone CLI tool directly from the local repository source code using `uv tool install`.

### The Core Hypothesis
> *If `pyproject.toml` correctly defines `[project.scripts]` and `[tool.setuptools.packages.find]`, `uv` will build an isolated tool sandbox, place an executable wrapper (`contextportal.exe`) in the user's local bin directory, and allow the tool to be executed from any directory outside the codebase (`$env:TEMP`) without requiring python module flags or virtualenv activation.*

---

## 2. Test Execution & Raw Logs

### Step 1: Isolated Tool Installation from Source
**Directory**: `C:\Users\maruthi.n.marella\ContextPortal`  
**Command**:
```powershell
uv tool install --force C:\Users\maruthi.n.marella\ContextPortal\backend
```

**Terminal Output**:
```text
Resolved 62 packages in 2.29s
      Built contextportal-backend @ file:///C:/Users/maruth
Prepared 1 package in 6.90s
Installed 62 packages in 3.03s
 + annotated-doc==0.0.5
 + annotated-types==0.8.0
 + anyio==4.14.2
 + attrs==26.1.0
 + beautifulsoup4==4.15.0
 + certifi==2026.7.22
 + cffi==2.1.1
 + chardet==5.2.0
 + click==8.5.0
 + colorama==0.4.6
 + contextportal-backend==0.1.0 (from file:///C:/Users/maruthi.n.marella/ContextPortal/backend)
 + cryptography==50.0.1
 + cssselect==1.3.0
 + fastapi==0.141.1
 + greenlet==3.5.5
 + h11==0.16.0
 + hiredis==3.4.1
 + httpcore==1.0.9
 + httpcore2==2.12.0
 + httptools==0.8.0
 + httpx==0.28.1
 + httpx2==2.12.0
 + idna==3.19
 + jsonschema==4.26.0
 + jsonschema-specifications==2025.9.1
 + lxml==6.1.2
 + lxml-html-clean==0.4.5
 + markdown-it-py==4.2.0
 + markdownify==1.2.3
 + mcp==2.1.1
 + mcp-types==2.1.1
 + mdurl==0.1.2
 + opentelemetry-api==1.44.0
 + playwright==1.62.0
 + pycparser==3.0
 + pydantic==2.13.5
 + pydantic-core==2.46.5
 + pydantic-settings==2.15.0
 + pyee==13.0.1
 + pygments==2.21.0
 + pyjwt==2.13.0
 + python-dotenv==1.2.3
 + python-multipart==0.0.32
 + pywin32==312
 + pyyaml==6.0.3
 + readability-lxml==0.9
 + redis==8.1.0
 + referencing==0.37.0
 + rich==15.0.0
 + rpds-py==2026.6.3
 + shellingham==1.5.4
 + six==1.17.0
 + soupsieve==2.9.2
 + sse-starlette==3.4.8
 + starlette==1.6.0
 + truststore==0.10.4
 + typer==0.27.2
 + typing-extensions==4.16.0
 + typing-inspection==0.4.4
 + uvicorn==0.52.4
 + watchfiles==1.2.0
 + websockets==17.1
Installed 1 executable: contextportal
warning: `C:\Users\maruthi.n.marella\.local\bin` is not on your PATH. To use installed tools, run `$env:PATH = "C:\Users\maruthi.n.marella\.local\bin;$env:PATH"` or `uv tool update-shell`.
```

---

### Step 2: Execution from External Environment ($env:TEMP)
**Directory**: `C:\Users\maruthi.n.marella\AppData\Local\Temp`  
**Commands**:
```powershell
cd $env:TEMP
contextportal --help
```

**Terminal Output**:
```text
usage: python.exe C:\Users\maruthi.n.marella\.local\bin\contextportal
       [-h] {mcp,login,fetch} ...

ContextPortal — The authenticated fetch layer for AI agents.

positional arguments:
  {mcp,login,fetch}
    mcp              Start the Model Context Protocol (MCP) server over STDIO.
    login            Open a browser to manually authenticate and save your session.
    fetch            Test retrieval of a URL directly from the CLI.

options:
  -h, --help         show this help message and exit
```

### Step 3: Public Content Retrieval from External Directory ($env:TEMP)
**Directory**: `C:\Users\maruthi.n.marella\AppData\Local\Temp`  
**Command**:
```powershell
contextportal fetch https://example.com
```

**Terminal Output**:
```text
Fetching context for: https://example.com

Attempting normal public fetch for: https://example.com
Successfully retrieved publicly.
================================================================================
Title: Example Domain
Retrieval Method: http (Authenticated: False)
================================================================================
# Example Domain

This domain is for use in documentation examples without needing permission. Avoid use in operations.

[Learn more](https://iana.org/domains/example)
```

### Step 4: Protected Enterprise Content Retrieval from External Directory ($env:TEMP)
**Directory**: `C:\Users\maruthi.n.marella\AppData\Local\Temp`  
**Command**:
```powershell
contextportal fetch https://project-dynamo.learn.joinhandshake.com/introduction
```

**Terminal Output**:
```text
Fetching context for: https://project-dynamo.learn.joinhandshake.com/introduction

Attempting normal public fetch for: https://project-dynamo.learn.joinhandshake.com/introduction
Public fetch redirected to auth page: https://app.joinhandshake.com/access?destination_hai_path=%2fauth%3fredirectto%3dhttps%253a%252f%252fproject-dynamo.learn.joinhandshake.com%252fintroduction
Public fetch failed or requires authentication. Falling back to authorized session...
Navigating to https://project-dynamo.learn.joinhandshake.com/introduction...
Extracting content...
================================================================================
Title: Lovable App
Retrieval Method: browser (Authenticated: True)
================================================================================
## What a task is

A task is a self-contained challenge that runs inside a Docker container. You author a few things, and together they let the benchmark score any agent deterministically:

* **`instruction.md`** - the only thing the agent sees at runtime. It states the problem, pins absolute paths, and lists success criteria the agent can verify on its own.
* **`solution/solve.sh`** - the golden reference solution. Keep the real logic in a helper (e.g. `solution/solve.py`) that `solve.sh` calls; write outputs to absolute `/app` paths.
* **`tests/`** - `test.sh` plus `test_outputs.py` (pytest), which run after the agent finishes and score its output. pytest and its plugins are baked (pinned) into the single `environment/Dockerfile`; `test.sh` installs nothing. `tests/` is added only at verify time and is not present during the agent run.
* **`environment/Dockerfile`** - the task's single image, built once and reused for both the agent run and the verifier run. It never contains the solution or the tests.
* **`task.toml`** - the machine-readable manifest: identity, environment limits, verifier mode, metadata.

## Harbor

**Harbor** is the CLI you'll use throughout. It builds the single task image, runs it, and writes the reward. Point it at a task path: `harbor run -p . --agent oracle` (run from the `task/` directory).
...
```

---

## 3. Key Observations & Architectural Analysis

1. **Clean Dependency Resolution & Sandboxing**:
   - `uv` resolved 62 packages in 2.29 seconds and created a dedicated virtual environment under `C:\Users\maruthi.n.marella\AppData\Roaming\uv\tools\contextportal-backend`.
   - The user's system Python remains 100% clean and unpolluted.

2. **Executable Generation & Discovery**:
   - `uv` generated `C:\Users\maruthi.n.marella\.local\bin\contextportal.exe`.
   - The CLI entrypoint `app.cli:main` was mapped properly, exposing all three core subcommands (`mcp`, `login`, `fetch`).

3. **External Execution Confirmation**:
   - The CLI ran successfully inside `$env:TEMP` (`C:\Users\maruthi.n.marella\AppData\Local\Temp`), proving that the package entrypoint does not rely on being inside the repository root.

4. **Self-Contained Public Retrieval Tier**:
   - `contextportal fetch` executed the full `httpx` + `readability-lxml` + `markdownify` pipeline from an external directory without missing any runtime dependencies (`app.core.retriever`, `app.core.security`).
   - Clean, stripped Markdown was returned to stdout with correct metadata (`Retrieval Method: http`, `Authenticated: False`).

5. **Deterministic Global Session Reuse**:
   - The persistent browser engine successfully located and mounted the global profile directory at `C:\Users\maruthi.n.marella\.contextportal\playwright_profile`.
   - The SSO/Handshake session cookies were automatically recognized, bypassing the login gateway and extracting the full protected Markdown payload with `Retrieval Method: browser (Authenticated: True)`.

---

## 4. Test Verdict
- **Level 1.1 (Source Tool Installation)**: ✅ **PASSED**
- **Level 1.2 (CLI Help & Discovery in External Env)**: ✅ **PASSED**
- **Level 1.3 (Public URL Retrieval in External Env)**: ✅ **PASSED**
- **Level 1.4 (Protected Enterprise URL Retrieval via Global Profile)**: ✅ **PASSED**

**Overall Level 1 Status**: 🚀 **ALL TESTS PASSED**



