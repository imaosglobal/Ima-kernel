# IMA Capability Factory

## Purpose

Turn a verified capability gap into a first-party IMA adapter/plugin when no suitable external integration exists.

## Lifecycle

`detected → specified → scaffolded → implemented → tested → verified → published → monitored → reassessed`

## Rules

1. Discovery is automatic; external account connection is not.
2. Never copy proprietary code, bypass authentication, scrape prohibited interfaces, or violate provider terms.
3. Prefer public APIs, SDKs, open standards, webhooks, and documented protocols.
4. Every adapter declares its provider, capabilities, auth requirements, limits, evidence, test status, and commercial terms.
5. A capability cannot be advertised as verified until an executable test produces evidence.
6. Provider-neutral interfaces should be used whenever possible so one provider can be replaced by another.
7. Commercialization must respect provider licenses and terms.
8. Revenue optimization considers user value, provider revenue, IMA revenue, operating cost, reliability, privacy, and risk.

## Adapter contract

Each adapter should expose:

- `id`
- `provider`
- `capabilities`
- `auth`
- `execute()`
- `health()`
- `evidence`
- `limits`
- `commercial`

## Commercial model

A first-party adapter may be packaged as:

- API
- SDK
- plugin/MCP server
- hosted service
- white-label integration
- marketplace listing

Possible commercial flows include subscription, usage pricing, licensing, referral revenue, or revenue sharing where contractually permitted.

## Evidence states

- `discovered`
- `connected`
- `authenticated`
- `executable`
- `tested`
- `verified`
- `generalized`

Unknown remains unknown until evidence exists.
