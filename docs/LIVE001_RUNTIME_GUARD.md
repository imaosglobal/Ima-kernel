# LIVE-001 Runtime Guard

Status: canonical runtime guardrail
Date: 2026-11-24

## Purpose

LIVE-001 is the canonical shared browser/device verification surface for IMA. It is a runtime dependency for website/app changes that require visual or interactive verification.

## Hard invariant

The Desktop Commander device used for the canonical live-browser path must remain continuously available to the extent the underlying device and Desktop Commander service support it.

Current canonical device:
- Desktop Commander device: localhost
- Device ID: 863839ba-718b-4553-b9ea-247cfb8980b8

An offline Desktop Commander state is a blocker. It must never be represented as a successful LIVE-001 connection.

## Verification chain

Before claiming LIVE-001 is usable, verify:

1. Desktop Commander device is online.
2. Canonical Termux IMA bridge is running.
3. Chrome/CDP is reachable.
4. BrowserGlass is reachable.
5. IMA Universal Action Core / MCP is reachable.
6. LIVE-001 reports available.
7. A real read-only observation succeeds.
8. A safe test action succeeds and its result is observed.

Code deployment is not runtime verification.

## Change gate

Until the verification chain is green, do not make or report visual/interactive website fixes as verified. Safe backend/documentation work may continue, but user-visible success claims remain blocked.

## Recovery rule

If Desktop Commander is offline, record:
- exact observed status;
- last-seen time;
- affected LIVE-001 capabilities;
- whether automatic recovery is technically available;
- the smallest required device-side recovery action.

Do not create a second browser surface or parallel bridge.

## Current evidence

On 2026-11-24 the canonical Desktop Commander device was observed Offline, last seen approximately 57 hours earlier. Therefore LIVE-001 is currently NOT runtime-verified.

The existing Termux bridge already has a canonical Android autostart path via Termux:Boot and a cloud device-agent path. That path is not evidence that Desktop Commander itself is online.

## Operating principle

observe -> map -> connect -> execute -> verify -> document -> reassess

No claim of "fixed", "connected", "live", or "runtime-verified" without evidence from the corresponding runtime layer.
