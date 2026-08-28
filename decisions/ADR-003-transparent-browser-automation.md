# ADR-003: Transparent Browser Automation (No Stealth Flags)

## Status
Accepted

## Context
When an authenticated resource is requested, ContextPortal falls back to a Playwright browser session (`_fetch_authenticated_sync`) to allow the user to legitimately authenticate and to execute client-side rendering.

During development, we observed that Google OAuth flows often block Playwright because Google detects the automated browser environment (e.g., `navigator.webdriver = true`) and displays a "This browser or app may not be secure" error.

It is possible to bypass these basic security checks by injecting stealth flags (e.g., `--disable-blink-features=AutomationControlled` or ignoring `--enable-automation`).

## Decision
1. **Use Real Chrome**: We will use the user's real installed Chrome browser (`channel="chrome"`) rather than the bundled Playwright Chromium, as it represents the user's legitimate environment.
2. **No Stealth or Evasion**: ContextPortal will **NOT** implement stealth flags, hide `navigator.webdriver`, or attempt to evade website security/bot controls. 
3. **Respect Upstream Security**: If a provider like Google decides an automated browser authentication flow is insecure, ContextPortal must respect that decision. We must not engage in an arms race to defeat authentication security.

## Rationale
ContextPortal's core mission is to act as an authorization-aware bridge, not a security-bypass tool. 
- "Make automation invisible so Google lets us through" is a malicious/scraping architecture.
- "Use the user's legitimately authorized browser session to retrieve resources they are legitimately allowed to access" is our product architecture.

## Consequences
- **Positive**: The system remains strictly within legitimate authentication bounds.
- **Positive**: We avoid the maintenance burden and arms race of maintaining stealth scraping infrastructure.
- **Negative**: Certain aggressive security providers (like Google OAuth) may natively block the automated window. Users will need to use fallback authentication methods (like OTP, Magic Links, or standard Username/Password) if the provider blocks the automated window.

## Guiding Principle for Agents
> **ContextPortal operates within legitimate authorization.** 
> Never attempt to hide automation flags, spoof fingerprints, bypass CAPTCHAs, or evade authentication controls. The user authenticates natively, and we only operate within the permissions granted by that authentication.

