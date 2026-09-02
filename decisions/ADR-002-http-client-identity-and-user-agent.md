# ADR-002: HTTP Client Identity and User-Agent Policy

## Status
**Accepted**

---

## Context
When ContextPortal executes its lightweight Tier 1 HTTP retrieval (`fetch_public`), it makes requests via `httpx.AsyncClient`. Previously, no custom `User-Agent` header was defined, resulting in the client broadcasting the underlying library's default string:

```text
User-Agent: python-httpx/0.28.1
```

While `python-httpx` is transparent about the protocol engine, it reflects an **implementation detail** rather than the **application identity**.

---

## Decision

1. **Explicit Application User-Agent for HTTP Tier**:
   The HTTP retrieval client will explicitly identify as ContextPortal with its version number and repository link:
   ```text
   User-Agent: ContextPortal/0.1.0 (+https://github.com/NavadeepDj/ContextPortal)
   ```

2. **Native Identity for Browser Tier (ADR-003)**:
   When ContextPortal escalates to the Tier 2 persistent browser engine (Playwright on Google Chrome), it will continue to broadcast Chrome's native User-Agent. This is legitimate because the request is executed by an actual Google Chrome process running on the user's host machine.

---

## Rationale & Architectural Benefits

* **Application Abstraction over Library Detail**: Decouples the public identity of ContextPortal from the specific HTTP client library used. If `httpx` is later swapped for another engine (e.g. `aiohttp`, `curl_cffi`), the application's external identity remains stable.
* **Operator Transparency ("The Visitor Badge")**: Web operators and server administrators can immediately understand what software is generating the automated requests and where to find documentation or report issues.
* **Professional Infrastructure Standard**: Mature developer tools declare their branded identity rather than relying on generic python script defaults.
* **No Sneaky Disguises**: ContextPortal does not spoof browser headers on simple HTTP requests. It identifies honestly as an automated context retrieval layer.

---

## Consequences & Verification
* The HTTP client will include `DEFAULT_HEADERS = {"User-Agent": "ContextPortal/0.1.0 (+https://github.com/NavadeepDj/ContextPortal)"}` in all outbound requests.
* Existing public retrieval and HTTP fallback tests must continue to pass without regression.

