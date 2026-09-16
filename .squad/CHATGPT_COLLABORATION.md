# IMA — Shared Claude + ChatGPT Work Protocol

Date: 2026-09-16

## Purpose

This file is the shared coordination point for Claude and ChatGPT working on the same IMA workspace.

The goal is not to create another parallel architecture. The goal is to turn the existing IMA work into one verified, working product.

## Current verified workspace

Primary repository:
`/data/data/com.termux/files/home/Ima-kernel`

The repository contains a very large historical/archive surface and many duplicated implementations. Do not treat file count or documented architecture as proof of runtime capability.

`IMA_CONTEXT.md` explicitly requires independent runtime verification.

## Operating rules

1. Inspect before changing.
2. Preserve existing working behavior.
3. Never delete or overwrite historical backups merely to simplify the tree.
4. Do not create another duplicate subsystem when an existing active implementation can be repaired or connected.
5. Separate documented capability from verified runtime capability.
6. Every implementation change must have a verification step.
7. Prefer small, reversible changes.
8. Record important discoveries and completed work here or in the relevant `.squad` logs.
9. If a tool/environment limitation prevents a test, record that fact instead of claiming success.
10. The human should not be used as an unnecessary execution bridge between agents when the shared filesystem can carry the information.

## Known environment limitation

Desktop Commander can read and write the Termux filesystem, but its current shell cannot execute Termux binaries such as `/data/data/com.termux/files/usr/bin/git`, `find`, `pm2`, or `bash` because they return `Permission denied`. Do not interpret those failures as IMA failures.

## Initial audit findings

- Primary workspace exists and is readable.
- IMA has substantial historical implementation material.
- `IMA_CANONICAL_VISION.md` defines the intended universal continuous-intelligence architecture.
- `IMA_CONTEXT.md` says the active runtime must be verified independently.
- `CANONICAL_ACTIVE_REGISTRY.json` names an intended active set including `IMA_START.py`, `ima_system.py`, `ima_runtime.py`, `ima_daemon.py`, and `ima.py`.
- `IMA_CAPABILITY_MAP.json` contains large counts of candidate implementations across memory, knowledge, truth, decision, learning, self-model, conversation, and reflection.
- `IMA_MISSING_CAPABILITIES_SCAN.json` also contains many historical candidates, so its presence alone is not proof that those capabilities are missing from the active runtime.
- The `.squad` directory already exists and contains orchestration logs/configuration.
- Claude's Desktop Commander history shows that Claude has already been inspecting this same device and the same IMA repository.

## Division of work

Claude: inspect and implement where appropriate, using the shared filesystem and existing project context.

ChatGPT: independently inspect the same workspace, verify claims, identify conflicts/duplication, design integration boundaries, and make directly verifiable changes when the environment permits.

Both agents must treat files as the shared state, not their private conversation history.

## Immediate mission

Establish a single verified path from:

human request -> IMA runtime -> memory/context -> intelligence/model -> response/action -> verification

Then connect product/UI/deployment surfaces to that verified path.

Do not declare the mission complete because documentation, scripts, backups, or registries exist.

## Handoff format

When making a substantive change, record:

- timestamp
- agent
- files changed
- reason
- verification performed
- result
- remaining uncertainty

## Current status

ChatGPT created this coordination file after inspecting the workspace on 2026-09-16.

No source code has been modified by ChatGPT during this audit.
