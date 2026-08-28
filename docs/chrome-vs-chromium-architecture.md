# Chrome vs. Chromium: Browser Engine Selection in ContextPortal

## Overview

When executing browser-level retrieval for protected or JavaScript-rendered web pages, Playwright offers two primary choices:
1. **Bundled Chromium**: The open-source, headless-optimized test-runner binary distributed with Playwright (`playwright install chromium`).
2. **Installed Google Chrome (`channel="chrome"`)**: The user's actual installed Google Chrome application on their operating system.

ContextPortal deliberately configures Playwright to launch **installed Google Chrome** (`channel="chrome"`). This document explains the technical, security, and architectural reasons behind this decision.

---

## 1. Summary of Differences

| Feature / Property | Bundled Playwright Chromium | Installed Google Chrome (`channel="chrome"`) | ContextPortal Choice |
|---|---|---|---|
| **Binary Source** | Test-specific Chromium build in AppData cache | System-installed Chrome (`Program Files` / `Applications`) | **Installed Chrome** |
| **Media Codecs** | Open codecs only (VP8/VP9, Opus, WebM) | Full proprietary codecs (H.264, AAC, MP3, MP4) | **Installed Chrome** (Renders all enterprise media) |
| **Identity Provider Trust** | Frequently flagged as synthetic test runner | Treated as standard consumer browser binary | **Installed Chrome** (Higher auth success rate) |
| **OS & Enterprise Trust** | Isolated from system trust store | Inherits OS root certificates, enterprise CAs, proxy rules | **Installed Chrome** (Works in enterprise corporate networks) |
| **Philosophical Match** | Scraping / automated testing bot | Authentic user environment context bridge | **Installed Chrome** (Legitimate context bridge) |

---

## 2. Technical Advantages of Real Chrome

### A. Proprietary Codecs and Rich Media Rendering
Bundled Chromium is strictly open-source and lacks licensing for proprietary media codecs (such as H.264 video and AAC audio). 

Modern enterprise documentation platforms, video learning portals (e.g., Handshake Dynamo, Coursera, internal LMSs), and interactive dashboards often embed rich media or HTML5 video/canvas components. If an agent requests content from a page that relies on these components to trigger DOM completion, bundled Chromium can fail or render placeholder errors, whereas real Chrome renders the page completely.

### B. Enterprise Network, Proxy, and Certificate Integration
In corporate environments, traffic frequently passes through enterprise forward proxies, VPNs, or requires custom internal Root Certificate Authorities (CAs).
- **Bundled Chromium** runs in a sandbox with default NSS/OpenSSL stores that may not trust internal corporate certificates, resulting in `ERR_CERT_AUTHORITY_INVALID` errors.
- **Installed Google Chrome** natively binds to the Windows Certificate Store (`certmgr.msc`) and macOS Keychain, seamlessly trusting company VPNs, intranet certificates, and enterprise Single Sign-On (SSO) portals.

### C. Authentic Rendering and Font Engines
Installed Chrome includes platform-specific font rendering optimizations, color profiles, and GPU acceleration features matching the user's display, ensuring that layout-sensitive DOM extraction produces accurate text flows and Markdown hierarchies.

---

## 3. The Identity Provider & OAuth Challenge

When interacting with modern web applications protected by Google Sign-In, Microsoft Entra ID (Azure AD), Okta, or Apple ID, authentication security systems inspect the incoming browser environment.

### Why Bundled Chromium Fails Google OAuth
Playwright's bundled Chromium binary is compiled specifically for test automation. Google OAuth actively monitors for test automation indicators. When a user attempts to log into Google via bundled Chromium, Google often blocks the flow with:
> *"This browser or app may not be secure. Learn more. Try using a different browser."*

### Why `channel="chrome"` Improves Compatibility
By launching the installed Chrome executable via `channel="chrome"`, the underlying executable signature matches the genuine consumer browser. While automated control is still transparently declared (see below), the binary integrity and environment match standard Chrome distributions.

---

## 4. Architectural Philosophy: Authenticity without Evasion

Choosing real Chrome is strictly aligned with ContextPortal's **Security and Automation Philosophy** (see `docs/security-and-automation-philosophy.md` and `decisions/ADR-003-transparent-browser-automation.md`):

### What We DO:
```python
browser_context = p.chromium.launch_persistent_context(
    user_data_dir="./playwright_profile",
    headless=False,
    channel="chrome",  # Launch the user's authentic Chrome installation
    viewport={"width": 1280, "height": 800}
)
```
- We launch the user's genuine browser.
- We allow the user to legitimately complete login and MFA.
- We maintain session state in an isolated local directory.

### What We DO NOT Do:
- We **do not** inject stealth scripts to mask `navigator.webdriver`.
- We **do not** pass flags like `--disable-blink-features=AutomationControlled` to evade bot detection.
- We **do not** bypass CAPTCHA or security challenges.

ContextPortal's objective is to be an **authorized context bridge representing the user**, not an evasive scraper. Using real installed Chrome represents the most faithful, secure, and transparent realization of that objective.

