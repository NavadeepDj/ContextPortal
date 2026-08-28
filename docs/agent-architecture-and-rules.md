# Agent Instruction Files & Architecture Overview

This document explains the purpose and relationship between the different agent instruction files in ContextPortal.

---

## 1. Source of Truth Hierarchy

1. **Product Thesis**: [`docs/PRODUCT_THESIS.md`](../docs/PRODUCT_THESIS.md) — The authoritative product definition. Read this first.
2. **Engineering Rules**: [`AGENT_RULES.md`](../AGENT_RULES.md) — Security boundaries and coding standards.
3. **Implementation Plan**: [`IMPLEMENTATION_PLAN.md`](../IMPLEMENTATION_PLAN.md) — Current phase and next steps.
4. **Architecture Decisions**: [`decisions/`](../decisions/) — ADRs for key architectural choices.
5. **Source Code & Tests**: Always authoritative over documentation.
6. **OpenWiki**: [`openwiki/`](../openwiki/quickstart.md) — Auto-generated codebase index.

> **Note:** `PROJECT_SPEC.md` was written before the product reset and is superseded by `PRODUCT_THESIS.md`. It is kept for historical reference only.

---

## 2. File Responsibilities

| File | Purpose | Loaded By |
|---|---|---|
| **`docs/PRODUCT_THESIS.md`** | Core product definition: ContextPortal is an authenticated fetch layer, not a browser automation app | Read by agents and humans before any implementation |
| **`AGENT_RULES.md`** | Deep security rules, coding standards, ephemeral proxy guidelines | Read by agents for implementation guidance |
| **`AGENTS.md`** | High-level repository instructions & OpenWiki pointer | Auto-loaded by Antigravity / agent runtimes |
| **`CLAUDE.md`** | Compatibility redirect pointing to `AGENTS.md` | Auto-loaded if using Claude Code CLI |

---

## 3. Detailed Breakdown

### `docs/PRODUCT_THESIS.md` — The Product Reset Directive
* Defines ContextPortal as **"The authenticated fetch layer for AI agents."**
* Establishes the core abstraction: Agent provides a URL → ContextPortal handles retrieval → Agent receives clean Markdown.
* Explicitly states what ContextPortal is NOT (browser automation product, RAG system, data warehouse).
* Defines the phased development strategy (A through F).
* Must be read before implementing any feature.

### `AGENT_RULES.md` — The Security & Engineering Contract
* Comprehensive 29-rule engineering handbook written specifically for ContextPortal.
* Enforces critical security boundaries:
  * Never collect or store third-party credentials.
  * Ephemeral proxy model: never persist private webpage content permanently.
  * Mandatory SSRF protection, isolated browser sessions, and token revocation.
  * Definition of Done (TDD, tests must pass).

### `AGENTS.md` — The Antigravity & Agent Entry Point
* Automatically injected by Antigravity IDE and modern coding agents at the start of every session.
* Contains the `<!-- OPENWIKI:START -->` hook informing agents of the `openwiki/` index.
* Instructs agents that source code and test suites remain authoritative over generated wiki pages.

### `CLAUDE.md` — The Claude Code CLI Compatibility Pointer
* Lightweight compatibility redirect.
* Forwards Anthropic Claude Code CLI instances to read `AGENTS.md` so that all agent tools follow the same single source of truth.
