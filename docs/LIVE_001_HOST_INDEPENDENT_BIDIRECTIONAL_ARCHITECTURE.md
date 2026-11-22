# LIVE-001 — Host-Independent Bidirectional Architecture

Status: active canonical direction
Date: 2026-11-22

## Decision

LIVE-001 must not depend on ChatGPT Free being able to host custom MCP Apps.

IMA remains the canonical product and execution host. ChatGPT is an optional external host/provider. When ChatGPT enables the required capability for Ori's account, the same LIVE-001 MCP/UI contract should be enabled as a second host rather than replacing the IMA host.

## Bidirectional model

```
                    ┌───────────────┐
                    │   IMA Core    │
                    │ intelligence  │
                    │ consent/state │
                    └───────┬───────┘
                            │
                    canonical MCP/UI
                            │
              ┌─────────────┴─────────────┐
              │                           │
      ┌───────▼────────┐         ┌────────▼────────┐
      │   IMA Host     │         │  ChatGPT Host   │
      │ primary now    │         │ optional/when   │
      │                │         │ eligible        │
      └───────┬────────┘         └────────┬────────┘
              │                           │
              └─────────────┬─────────────┘
                            │
                       BrowserGlass
                            │
                    IMA Device Bridge
                            │
                    Android / Chrome
                            │
                         result
                            │
                  ──────────┴──────────
                    back to IMA Core
```

## Required directionality

1. IMA → ChatGPT: expose canonical MCP tools/resources/UI when ChatGPT permits the account.
2. ChatGPT → IMA: tool calls, UI events, results and user-approved actions must return through the same canonical IMA session/provenance layer.
3. IMA → device/browser: only consented, authorized actions.
4. Device/browser → IMA: verified state/result, never an assumed success.
5. The same action/result contract must work with IMA Host and ChatGPT Host.

## Activation rule

Do not create a second LIVE system when ChatGPT becomes eligible.

When authoritative evidence confirms that this account can use custom MCP Apps/runtime UI:
- verify the actual account/surface capability;
- enable the existing ChatGPT-host adapter for LIVE-001;
- run the canonical end-to-end QA;
- record evidence in the LIVE-001 journal;
- keep IMA Host active as the independent fallback.

If the capability is not available, keep the IMA Host path active and continue monitoring. No workaround or policy bypass is permitted.

## Monitoring

OpenAI support cases #20595626 and #19768893 remain the authoritative account-specific thread. Monitor that thread and OpenAI's current public documentation for changes to Free-plan MCP Apps/runtime availability.

## Acceptance

LIVE-001 is complete only when at least one host can perform the full verified loop:

request → consent → MCP/tool call → BrowserGlass → authorized Android/Chrome action → observed result → result returned to IMA → provenance/QA record.

ChatGPT hosting is an additional host capability, not a prerequisite for IMA itself.


## Multi-intelligence federation

LIVE-001 is not limited to ChatGPT.

IMA should act as a canonical interoperability layer for any legitimately connected intelligence, model, agent, assistant, or host that exposes a supported interface. The direction is intentionally bidirectional:

- IMA → connected intelligence: send an authorized request/context/tool/resource.
- Connected intelligence → IMA: return an answer, capability, tool result, event, or evidence.
- IMA → another connected intelligence: route only when authorized and useful.
- Results → IMA: normalize provenance, permissions, uncertainty, source and verification state before reuse.
- IMA → user: present the result without implying that one intelligence is another or that a result is verified when it is not.

This creates a federation rather than a dependency: ChatGPT is one possible host/intelligence; other compatible systems can participate through the same canonical contract.

No intelligence receives another user's private data by default. Identity, authorization, consent, data scope and provenance remain explicit at every hop. Cross-intelligence routing must be auditable and must not silently expand permissions.

The economic objective is lawful value creation through interoperability, accessibility, user productivity, distribution, services and future commercial integrations. Revenue is never claimed until actually measured.

