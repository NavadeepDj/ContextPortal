# Agent Instruction Files & Architecture Overview

This document explains the purpose and relationship between the different agent instruction files in ContextPortal.

---

## 1. File Responsibilities

| File | Purpose | Loaded By |
|---|---|---|
| **`AGENT_RULES.md`** | Deep security rules, coding standards, ephemeral proxy guidelines | Read by agents for implementation guidance |
| **`AGENTS.md`** | High-level repository instructions & OpenWiki pointer | Auto-loaded by Antigravity / agent runtimes |
| **`CLAUDE.md`** | Compatibility redirect pointing to `AGENTS.md` | Auto-loaded if using Claude Code CLI |

---

## 2. Detailed Breakdown

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
