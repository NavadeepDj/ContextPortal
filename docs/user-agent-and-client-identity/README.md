# HTTP Client Identity & User-Agent Policy (ADR-002)

## 1. Executive Summary & Philosophy

ContextPortal is designed to be **legitimate developer infrastructure**—the authenticated context proxy for autonomous AI agents.

Because ContextPortal will be used by thousands of AI agents making automated requests across the public and private web, it must adhere to the highest standards of **web transparency and responsible internet citizenship**.

---

## 2. What is a User-Agent? (The "Visitor Badge" Analogy)

Whenever ContextPortal issues an HTTP request, the web server doesn't just receive `GET /page`. It receives metadata headers, including the `User-Agent`.

Think of the `User-Agent` as a **visitor badge** worn when entering a building:
* **The Disguise (Anti-Pattern)**: Telling building security *"I'm Chrome"* when you're actually a Python script.
* **The Library Default**: Wearing a generic badge that says *"Python Library"*.
* **The Responsible Citizen (ContextPortal)**: Wearing a clear badge that says:
  ```text
  ContextPortal/0.1.0 (+https://github.com/NavadeepDj/ContextPortal)
  ```

---

## 3. Application Identity vs. Library Implementation Detail

Before ADR-002, our HTTP retriever did not specify a custom `User-Agent`, which caused `httpx` to send its default string:

```text
User-Agent: python-httpx/0.28.1
```

### Why Moving Away from `python-httpx` Matters:

| Dimension | Library Default (`python-httpx`) | Application Identity (`ContextPortal/0.1.0`) |
|---|---|---|
| **Abstraction Level** | Leaks the underlying Python package. | Declares the actual software application. |
| **Refactor Resilience** | If we switch from `httpx` to `aiohttp` or `curl_cffi`, our external identity changes. | Identity remains stable across any internal client refactors. |
| **Server Operator Clarity** | Website administrators see generic Python scraper traffic. | Administrators see a link to our public repository and purpose. |
| **Professional Grade** | Looks like an ad-hoc local script. | Operates as recognized open-source infrastructure. |

---

## 4. The Two-Tier Architecture Distinction

ContextPortal operates a distinct two-tier retrieval model, and each tier handles identity differently:

```text
                           ContextPortal Retrieval
                                      │
                   ┌──────────────────┴──────────────────┐
                   ▼                                     ▼
        Tier 1: Lightweight HTTP               Tier 2: Browser Engine
                   │                                     │
         Uses Python HTTP client               Launches Real Chrome (ADR-003)
                   │                                     │
                   ▼                                     ▼
     User-Agent: ContextPortal/0.1.0       User-Agent: Real Google Chrome
```

### Tier 1: Lightweight HTTP (`fetch_public`)
* **Identity**: `ContextPortal/0.1.0 (+https://github.com/NavadeepDj/ContextPortal)`
* **Rule**: Never disguise HTTP scripts as browsers. Identify honestly as an automated context extractor.

### Tier 2: Persistent Browser Engine (`_fetch_authenticated_sync`)
* **Identity**: Native Google Chrome User-Agent (`Mozilla/5.0 ... Chrome/...`)
* **Rule**: Because ADR-003 attaches directly to the user's installed Google Chrome binary on their local machine, broadcasting Chrome's native header is 100% genuine and legitimate.

---

## 5. Why Make This Change Now?

When building an early prototype, the only goal is:
> *"Make it work."*

As ContextPortal moves toward **Phase C package distribution and PyPI release**, the goal matures to:
> *"Make it work **responsibly** and **transparently**."*

Establishing our application identity now prevents future breaking changes and ensures our open-source release represents clean, production-ready engineering.

---

## 6. Verification & Impact

- **Test Suite**: All 23 unit and integration tests pass with the new header.
- **Public Fetching**: Verified that standard documentation domains (e.g. `https://example.com`) continue to return clean Markdown without rejection.
- **Fallback Guarantee**: If any public site ever rejects the `ContextPortal` User-Agent, ContextPortal's automated tier-escalation safely falls back to the browser engine.
