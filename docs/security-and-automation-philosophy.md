# Security and Automation Philosophy

ContextPortal is designed to be an **authorization-aware context layer for AI agents**. It allows an agent to access authenticated resources securely, as easily as providing a link.

Because ContextPortal handles highly sensitive authenticated browser sessions, its security and automation philosophy must be strictly defined and rigorously enforced. 

This document outlines the core principles that separate ContextPortal from conventional web scrapers or browser-control agents.

---

## 1. The Core Principle: A Context Bridge, Not a Scraper

ContextPortal is a **bridge**, not a bypass. 

The system operates strictly within the permissions and authorizations legitimately granted by the user. 
- We do not "make automation invisible so Google lets us through." 
- We instead say: *"Use the user's authorized browser session to retrieve resources they are legitimately allowed to access."*

If a security provider (like Google OAuth) determines that an automated browser authentication flow is insecure, ContextPortal must **respect that decision**. We do not engage in an arms race to defeat authentication security, hide automation, or spoof fingerprints.

---

## 2. Transparent Automation (ADR-003)

When an authenticated resource requires a browser session (e.g., executing client-side rendering or waiting for a user to log in), ContextPortal delegates this task to Playwright.

### Permitted Behaviors
- **Using the Real Browser**: ContextPortal uses the user's real installed browser (e.g., `channel="chrome"`) rather than a bundled testing binary. This accurately reflects the user's legitimate environment.
- **Persistent Profiles**: ContextPortal utilizes a persistent, isolated local browser profile to securely store the user's authentication cookies and session state.

### Prohibited Behaviors
ContextPortal must **never** attempt to evade detection by injecting stealth flags or altering browser fingerprints. Future development must explicitly avoid:
- `--disable-blink-features=AutomationControlled`
- Ignoring `--enable-automation` flags
- Attempting to overwrite or hide `navigator.webdriver`
- Using stealth-scraping plugins

---

## 3. Honest HTTP Identity (ADR-002)

ContextPortal utilizes a tiered retrieval architecture. It attempts a fast, direct HTTP fetch first, falling back to a browser only when necessary.

### The Rule of Honest Identification
> **User-Agent is identification, not authentication.**

- ContextPortal's direct HTTP client (`httpx`) must send a centralized, descriptive User-Agent string (e.g., `ContextPortal/<version>`).
- The HTTP client must **never** spoof a Chrome or Safari User-Agent to bypass basic bot-protection policies on public websites.
- If a task genuinely requires browser-level execution, rendering, or an authenticated user session, the system must delegate to the actual Playwright/Chromium browser rather than forcing Python to pretend it is Chrome.

---

## 4. Strict Agent Boundaries

The most significant security risk in ContextPortal is exposing the authenticated browser session directly to the AI agent. To mitigate this, ContextPortal enforces strict abstraction boundaries.

### 🔐 1. Isolate the Browser Profile
The persistent browser profile (`./playwright_profile`) contains the user's cookies, session tokens, and authentication state. **This profile must never be exposed to the agent.** The agent receives only the extracted, sanitized Markdown content.

### 🔐 2. No Arbitrary Browser Control
ContextPortal is **not** a browser-control agent. 
The system workflow is:
```text
Agent -> "Give me content from this URL" -> ContextPortal -> Browser -> Clean Markdown
```
The workflow is **never**:
```text
Agent -> "Click this button, run this JavaScript, read these cookies" -> Browser
```
Allowing the agent to arbitrarily control the authenticated browser would convert ContextPortal into a dangerous security liability.

### 🔐 3. Human-Controlled Authentication
Authentication flows (entering passwords, solving CAPTCHAs, approving MFA requests) must remain fully human-controlled. 
- ContextPortal must never receive, intercept, or store the user's passwords.
- The user completes the authentication natively in the Playwright window. ContextPortal simply waits for the state to resolve and then extracts the requested resource.

