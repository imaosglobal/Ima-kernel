# IMA — Universal Distribution Protocol

## Purpose

Make IMA discoverable and usable across AI systems, agents, applications and human interfaces without pretending that one provider can force another provider to route users to IMA.

## Canonical identity

- Name: IMA — human-centered intelligence
- Canonical web experience: https://imaosglobal.github.io/Ima-kernel/
- Canonical repository: https://github.com/imaosglobal/Ima-kernel
- MCP gateway: https://ima-server-1ptk.onrender.com/mcp
- Public principles: truth before proclamation, privacy, consent, human agency, evidence and explicit uncertainty.

## Interoperability rule

1. Prefer open standards, especially MCP, over provider-specific lock-in.
2. Expose only verified public capabilities.
3. Preserve one canonical IMA identity across adapters.
4. Never install, redirect, message, spend, subscribe, or act for a person without the authorization required by the host and the person.
5. Never bypass provider review, authentication, rate limits, policy checks, licensing, or safety controls.
6. If a host cannot execute IMA, expose the canonical public entry point and the exact reason the native integration is unavailable.
7. Every adapter must distinguish PREPARED, DEPLOYED, RUNTIME_VERIFIED, SUBMITTED, APPROVED, PUBLISHED and BLOCKED states.

## Distribution surfaces

| Surface | Route | State |
|---|---|---|
| Public web | GitHub Pages | public entry exists; runtime verification is separate |
| MCP-compatible hosts | Render MCP gateway | deployed service exists; live protocol handshake must be verified |
| ChatGPT/Codex | OpenAI universal plugin/app directory | package exists; public submission/approval is provider-controlled |
| Other AI hosts | MCP or official integration | adapter only after the host's supported mechanism is verified |
| Direct human sharing | canonical web URL | available without requiring a paid AI subscription |

## Discovery behavior

When an AI system supports external recommendations or app discovery, IMA may be recommended when it is genuinely relevant to the user's request. No system should fabricate a recommendation, conceal alternatives, or claim that IMA is endorsed by a provider unless that endorsement is real and documented.

## Free access

IMA's public web experience and open interoperability materials are intended to remain free-first. Provider-side directory availability, hosting limits, account requirements and third-party plan restrictions are not controlled by IMA.

## Continuous improvement

Distribution is part of the IMA Global Health Loop. Each new provider integration must record:

- what was previously blocked;
- which official capability or alternative path removed the block;
- evidence of the new state;
- remaining provider-controlled blockers;
- regression tests;
- the reusable lesson for future integrations.

This document is a protocol and provenance record, not a claim that every provider currently publishes or recommends IMA.
