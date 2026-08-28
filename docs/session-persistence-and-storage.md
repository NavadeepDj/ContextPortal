# Session Persistence and Storage Architecture in ContextPortal

## Overview

A core capability of ContextPortal is providing AI agents seamless access to authenticated resources without forcing a human user to repeatedly solve login prompts. 

This document explains how **session persistence** is architected, how the local browser storage engine operates, and details a real-world case study from our Phase A testing with protected enterprise learning portals.

---

## 1. The Core Architecture: Stateless API + Persistent Browser Storage

A common question is: *Does the FastAPI backend store your passwords, session tokens, or login cookies in a database?*

**No.** The backend architecture is strictly decoupled:

```text
┌────────────────────────────────────────────────────────┐
│ FastAPI Backend (Stateless Application Layer)          │
│ • Validates URLs                                       │
│ • Coordinates tiered fetch (Public HTTP -> Browser)   │
│ • Runs extraction pipeline (HTML -> Markdown)          │
│ • NEVER stores cookies, passwords, or tokens in DB     │
└───────────────────────────┬────────────────────────────┘
                            │ Delegates to
                            ▼
┌────────────────────────────────────────────────────────┐
│ Playwright Persistent Browser Context (Local Engine)   │
│ • Launches real Chrome via user_data_dir               │
│ • Rooted at: ./backend/playwright_profile              │
│ • Stores: Cookies, localStorage, IndexedDB, Sessions   │
│ • Encrypted & managed natively by the Chrome engine    │
└────────────────────────────────────────────────────────┘
```

### Why This Design Matters
1. **Zero Credential Exposure**: The API application and AI agents never directly touch raw cookie strings, bearer tokens, or user passwords.
2. **Native Web Standard Compatibility**: Complex modern auth schemes (HTTP-only cookies, SameSite policies, WebAuthn, IndexedDB tokens) are handled natively by the browser engine exactly as intended by the identity provider.
3. **Local Isolation**: Each ContextPortal instance maintains its isolated profile on the user's local disk.

---

## 2. Real-World Lifecycle: The Handshake Verification Case Study

During Phase A validation, ContextPortal was tested against a real-world protected URL:
`https://project-dynamo.learn.joinhandshake.com/introduction`

Here is the exact step-by-step breakdown of how session persistence performed across two consecutive requests.

---

### Step 1: Cold Start — First Request (Auth Required)

The user submitted the protected URL to ContextPortal:
`GET /c?url=https://project-dynamo.learn.joinhandshake.com/introduction`

#### Execution Log:
```text
Attempting normal public fetch for: https://project-dynamo.learn.joinhandshake.com/introduction
Public fetch redirected to auth page: https://app.joinhandshake.com/access?destination_hai_path=%2fauth%3fredirectto%3dhttps%253a%252f%252fproject-dynamo.learn.joinhandshake.com%252fintroduction
Public fetch failed or requires authentication. Falling back to authorized session...
Navigating to https://project-dynamo.learn.joinhandshake.com/introduction...
Authentication required. Please log in using the opened browser window.
Waiting for you to complete login (up to 5 minutes)...
```

#### What Happened Under the Hood:
1. **Public Probe**: `httpx` made a lightweight HTTP GET request to check if the page was public.
2. **Redirect Interception**: The server returned a redirect to `app.joinhandshake.com/access` (an SSO gateway). ContextPortal detected the auth redirect and aborted the public fetch immediately.
3. **Browser Spawning**: ContextPortal launched Chrome with `user_data_dir="./playwright_profile"`.
4. **Login Detection**: ContextPortal inspected the page, detected the `/access` auth indicator, and paused execution for up to 5 minutes while displaying a clean prompt.
5. **Human Login**: The user entered their credentials (OTP/email sign-in) in the Chrome window.
6. **State Persistence**: Once authenticated, the browser wrote Handshake's session cookies and localStorage to `./backend/playwright_profile`.
7. **Extraction & Response**: ContextPortal detected that the page redirected to the target domain, extracted clean Markdown, and returned `200 OK`.

---

### Step 2: Warm Retrieval — Subsequent Request (Zero Human Interaction)

Shortly after, the user requested another protected page within the same domain:
`GET /c?url=https://project-dynamo.learn.joinhandshake.com/overview`

#### Execution Log:
```text
Attempting normal public fetch for: https://project-dynamo.learn.joinhandshake.com/overview
Public fetch redirected to auth page: https://app.joinhandshake.com/access?destination_hai_path=%2fauth%3fredirectto%3dhttps%253a%252f%252fproject-dynamo.learn.joinhandshake.com%252foverview
Public fetch failed or requires authentication. Falling back to authorized session...
Navigating to https://project-dynamo.learn.joinhandshake.com/overview...
Extracting content...
INFO:     127.0.0.1:62156 - "GET /c?url=https://project-dynamo.learn.joinhandshake.com/overview HTTP/1.1" 200 OK
```

#### What Happened Under the Hood:
1. **Public Probe Failed**: Fast HTTP check detected the auth redirect as usual.
2. **Browser Re-use**: Playwright opened Chrome pointing to the same `user_data_dir="./playwright_profile"`.
3. **Instant Session Recognition**: Handshake's servers inspected the cookies loaded from the persistent directory and immediately recognized the user's active session.
4. **No Login Prompt**: `is_login_page` evaluated to `False`. The browser navigated straight to the target content without stopping.
5. **Sub-second Extraction**: Clean Markdown was extracted and returned to the caller instantly.

---

## 3. Storage Directory Structure

The persistent storage directory resides in the backend repository root:

```text
backend/
├── app/
│   ├── core/
│   │   └── retriever.py    # References user_data_dir = "./playwright_profile"
│   └── main.py
└── playwright_profile/     # Created automatically by Chrome
    ├── Default/
    │   ├── Cookies         # SQLite database containing session cookies
    │   ├── Local Storage/  # HTML5 localStorage key-value pairs
    │   ├── IndexedDB/      # Client-side structured storage
    │   └── Network/        # Persistent network state & cache
    └── Local State         # Browser-level preferences & encryption keys
```

> [!IMPORTANT]
> The `./playwright_profile` directory is added to `.gitignore` and must **never** be committed to version control or synced to public repositories, as it holds live local session credentials.

---

## 4. Managing and Resetting Sessions

Because session management is fully tied to the local profile folder:

### To Log Out or Clear All Stored Sessions:
Stop the server and delete the `playwright_profile` directory:
```powershell
# In PowerShell:
Remove-Item -Recurse -Force ./backend/playwright_profile
```

On the next protected request, ContextPortal will generate a clean profile and prompt for authentication again.

### Session Lifespans:
ContextPortal does not artificially expire sessions. Session duration is dictated by the upstream service (e.g., Handshake, Jira, Notion, GitHub):
- If the service grants a 30-day session cookie, ContextPortal remains authenticated for 30 days.
- If the service invalidates the session or token, ContextPortal automatically catches the redirect and displays the login prompt again.

