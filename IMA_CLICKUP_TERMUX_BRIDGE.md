# IMA — ClickUp / GitHub / Termux Bridge

Status: CONNECTED_WORKSPACE_LAYER

## Canonical sources
- GitHub: https://github.com/imaosglobal/Ima-kernel
- Local Termux checkout: ~/Ima-kernel
- Local branch observed: main
- Remote observed: origin -> https://github.com/imaosglobal/Ima-kernel

## Operating contract
ClickUp is an execution/coordination layer. GitHub and the Termux checkout remain source-of-truth engineering artifacts.
IMA work must preserve creator identity, provenance, existing working functionality, reversibility, and verification.

Before a change:
1. inspect current state;
2. identify the exact goal and affected components;
3. preserve a rollback path;
4. make the smallest useful change;
5. test/verify;
6. record the result in GitHub and ClickUp.

Never silently overwrite local work. Never claim completion without evidence.

## Current canonical direction
VISION -> IDENTITY -> MISSION -> CAPABILITY -> IMPLEMENTATION -> VERIFICATION

IMA is intended as a human-centered continuous intelligence ecosystem with memory, learning, tools, action, perception, creativity, and long-term continuity.

## Local evidence observed
The Termux checkout contains:
- IMA_CANONICAL_VISION.md
- IMA_IDENTITY.md
- IMA_PUBLIC_README.md
- IMA_API_DOCUMENTATION.md
- extensive runtime, audit, memory, preservation, UI, deployment, and backup material
- multiple historical/backup IMA implementations

This bridge file is intentionally non-secret. Credentials, API keys, private memory, and local secrets must never be copied into ClickUp or public GitHub.

## ClickUp execution board
IMA — אמא / IMA Core & Continuous Improvement

The board is used to coordinate verified work against the actual GitHub + Termux state.
