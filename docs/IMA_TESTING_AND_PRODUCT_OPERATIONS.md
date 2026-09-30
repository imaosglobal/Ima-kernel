# IMA Testing & Product Operations

## Purpose

This is the permanent verification layer for IMA. Every change is treated as a product change, not only a code change.

## Verification pyramid

1. **Contract** — canonical identity, vision, registry, autonomy and provenance invariants.
2. **Unit/core** — memory, model/tool/agent gateways, derivation, action verification and self-hosted execution.
3. **Runtime** — Flask health, runtime capability contract, public chat, user isolation and rejection behavior.
4. **Frontend** — lint, production build, API configuration, UI bundle generation.
5. **Integration** — GitHub Pages build/deploy, Android APK build, backend deployment health.
6. **Security/privacy** — secret scan, public/private boundary, CORS allowlist, rate limiting, no unauthorized consequential actions.
7. **Product** — capability truthfulness, accessibility, responsive UI, 3D Mother presence, observability and provenance.
8. **Evolution** — scheduled health runs, failure issues, evidence retention and controlled improvements.

## Release gate

A release is considered verified only when the relevant automated checks pass. A green build alone is not sufficient evidence that a live backend is reachable.

## Continuous operation

The health workflow runs on pushes, manual dispatch and every six hours. Each scheduled run re-executes the verification gate defined in the workflow.

Future evolution must extend this harness before claiming a new capability as production-ready.

## Product management contract

Every new capability should have:

- a written product requirement
- an implementation owner/component
- an automated verification
- an observable runtime signal
- a privacy/security boundary
- a rollback or disable path
- provenance for external data and generated derivatives
- a documented current-status claim

## Free-first engineering

Prefer free/open-source or no-cost tiers for development, CI, testing and observability when they satisfy the requirement. Paid services may be integrated only when their capability is actually needed and their connection is explicit.

## No silent capability inflation

Documentation, UI and API status must not say that a model, site, device, memory system or external action is connected unless a live or deterministic verification demonstrates the connection.
