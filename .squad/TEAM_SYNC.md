# IMA — Shared Agent State

Date: 2026-09-16

## Agents

- ChatGPT — verification + integration
- Claude — implementation (session currently exhausted for today)
- Gemini — implementation/review continuation

## Source of truth

The shared repository and `.squad/` files are the coordination state.
Agents must inspect current files before changing code.

## Verified now

- Repository path exists: `/data/data/com.termux/files/home/Ima-kernel`
- `.squad/CLAUDE_HANDOFF.md` exists and requests continuation from actual repository state.
- `.squad/CHATGPT_COLLABORATION.md` exists and defines shared verification rules.
- `.squad/state.json` contains historical Squad cycle records.
- `.squad/runtime/` referenced by that state does not currently exist at the repository root.
- No Gemini-specific handoff file was found by directory listing.
- Desktop Commander can read/write the repository but its search facility currently lacks ripgrep.
- Earlier shell execution through the bridge returned Permission denied for Termux binaries.

## Current mission

Establish and verify one executable product path:

request -> context/memory -> intelligence -> response/action -> verification

Do not treat registries, backups, logs, or documentation as proof of runtime capability.

## Handoff rule

Each agent records substantive changes here or in a dedicated handoff file with:

1. timestamp
2. agent
3. files changed
4. reason
5. verification performed
6. result
7. remaining uncertainty
