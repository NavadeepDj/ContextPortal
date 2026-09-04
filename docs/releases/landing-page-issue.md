# Issue: Story-Driven Marketing Landing Page for ContextPortal

## 1. Problem Statement
The current frontend repository contains a bare default Next.js scaffold. As an open-source tool bridging MCP clients with local authenticated browser sessions, ContextPortal requires a high-impact, narrative-driven marketing landing page that:
1. Explains the core frustration (AI agents hitting login walls and asking humans for screenshots / copy-paste).
2. Illustrates the architecture and retrieval mechanism clearly ("One request. Zero credentials leaked.").
3. Provides an interactive retrieval simulation so developers immediately understand the product value before reading the codebase.
4. Conforms to modern, high-polish dark design aesthetics (Linear/Vercel style).

---

## 2. Proposed Scope & Deliverables
- **Design Foundation**:
  - Dark mode engineering canvas tokens (`globals.css`) with Tailwind CSS v4 `@theme inline`.
  - Component library primitives with `shadcn/ui` conventions (`Button`, `Card`, `Badge`).
  - Animation utilities and effects (`motion`, `Spotlight`, `Particles`, `BorderBeam`, `ShimmerButton`, `AnimatedBeam`).
  - Custom branded SVG logo (`logo.svg`) and typography.
- **Narrative Scroll Architecture (10 Sections)**:
  - `Navbar`: Sticky blurred header with brand identity, anchor navigation, and GitHub quick links.
  - `HeroSection`: Text generate effect headline, interactive URL input simulator with simulated multi-step retrieval log, and narrative emoji pipeline.
  - `ThePainSection`: "Without ContextPortal" timeline with staggered animation of the painful screenshot workflow.
  - `TheSolutionSection`: "There's a better way" with animated SVG data-flow beams across Agent → ContextPortal → HTTP/Browser → Clean Markdown.
  - `HowItWorksSection`: Three large cards with BorderBeam highlighting the 3-step lifecycle (Give URL → Authenticate once → Keep moving).
  - `DialogueSection`: Humorous dialogue comparing "Day 1 (First time)" vs "Day 2+ (Every time after)".
  - `PrivacySection`: Visual trust boundary demonstrating that session cookies remain strictly on local disk and never reach the agent.
  - `NotABrowserSection`: Clear side-by-side contrast between fragile "Browser Agents" vs resilient "Retrieval Tools".
  - `McpRevealSection`: Copyable MCP code snippet + architectural compatibility across Claude Desktop, Cursor, Antigravity, and VS Code.
  - `OpenSourceSection`: Open-source trust checklist and repository showcase card.
  - `FinalCtaSection`: Copyable `uv tool install contextportal` command with dual PyPI/GitHub action triggers.
  - `Footer`: Minimal legal, license, and author credits.

---

## 3. Acceptance Criteria
- [x] All 10 scroll sections render seamlessly without hydration mismatches.
- [x] Interactive hero simulator enables manual URL simulation and displays real-time retrieval logs.
- [x] Responsive layout works cleanly across mobile, tablet, and desktop viewports.
- [x] Next.js production build (`pnpm build`) succeeds with 0 errors and valid static HTML generation.
- [x] Root `.gitignore` updated to prevent caching artifacts (`.turbo/`, `*.tsbuildinfo`, `*.pem`, debug logs).
