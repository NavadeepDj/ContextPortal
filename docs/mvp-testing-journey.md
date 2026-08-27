# MVP Testing Journey: ContextPortal Retrieval Proof

This document chronicles the testing, errors, and iterative fixes encountered while proving Phase A of the ContextPortal MVP (The Retrieval Proof).

## 1. Initial Implementation
We implemented the core retrieval engine in `backend/app/core/retriever.py` with two paths:
*   `fetch_public`: A standard `httpx` GET request. It fell back to the authenticated path if it encountered HTTP 401 or 403.
*   `fetch_authenticated`: Used Playwright's `async_api` to launch a visible Chromium browser with a persistent context, allowing the user to manually log in if necessary.

## 2. First Test: The SPA Shell Issue
**The Test:** We requested a protected Handshake URL: `https://project-dynamo.learn.joinhandshake.com/introduction`.
**The Result:** The agent received a 200 OK, but the content was just markdown links to Facebook and LinkedIn tracking pixels. Playwright never opened.
**The Root Cause:** Handshake is a modern Single Page Application (SPA). Instead of returning a strict 401 Unauthorized, its servers returned a normal 200 OK along with an empty HTML shell. Client-side JavaScript then redirected the user to the login screen. Our naive `fetch_public` saw the 200 OK, parsed the empty shell (finding only tracking pixels), and returned it, believing it had succeeded.
**The Fix:** We updated `fetch_public` to be smarter about detecting auth walls:
1.  **Redirect Detection:** Check if the `final_url` after following redirects contains "login", "signin", or "auth".
2.  **Empty Content Heuristic:** If the extracted Markdown is suspiciously short (< 100 characters), assume it's an empty SPA shell and fail over to the authenticated path.

## 3. Second Test: The Windows Subprocess Bug
**The Test:** We re-ran the request for the Handshake URL with the improved `fetch_public` logic.
**The Result:** A 500 Internal Server Error. The logs showed a `NotImplementedError` originating from `asyncio.create_subprocess_exec`.
**The Root Cause:** This is a known issue with Python's `asyncio` on Windows when running within certain ASGI event loops (like uvicorn). Playwright's `async_api` attempts to spawn Chromium as a subprocess asynchronously, which the active event loop policy did not support.
**The Fix:** We rewrote the Playwright logic. Instead of using `playwright.async_api`, we switched to `playwright.sync_api`. To prevent blocking the FastAPI server, we wrapped the synchronous Playwright execution in `asyncio.to_thread()`, running it safely in a background thread.

## 4. Third Test: The Timeout Mystery
**The Test:** We re-ran the request with the threaded, synchronous Playwright implementation.
**The Result:** The Playwright browser successfully opened (bypassing the `NotImplementedError`)! However, the terminal logs showed a timeout.

Great progress! The Playwright browser actually opened this time (no more NotImplementedError!). But the issue is:

It said "Authentication required" and opened the browser
But then it said "Timeout waiting for manual login" - meaning the 5-minute timeout was hit
Wait, looking more carefully at the logs, it says "Timeout waiting for manual login" but the request returned 200 OK. That's interesting. It seems like it timed out on the login wait but still extracted content. Let me think about what happened...

Actually, looking at the timeline:

The request came in
It detected auth required
Browser opened
It said "Waiting for you to complete login (up to 5 minutes)..."
Then it timed out and ext
