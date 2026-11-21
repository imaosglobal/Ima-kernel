# IMA Legacy Capability Migration — 2026-11-21

## Decision

imaosglobal/Ima-kernel remains the sole canonical authority. Legacy repositories are provenance sources, not parallel runtimes.

## Migrated from Ima-3d-mom

Useful semantic intent detection was ported from kernel/brain_core.js into learning/legacy_capability_adapters.py.

The old file-based memory implementation and old action dispatcher were not copied. Their useful concepts are represented as action requests only; execution remains behind the canonical consent/action boundary and canonical memory authority.

## Audited from ima-os-evolving-home

Permanent-quality concepts were audited. Background fixers, rapid polling, mutation enforcement, and automatic UI rewriting were not copied as autonomous browser behavior. Those patterns could create duplicate or destructive control loops.

Reusable concepts are retained as requirements for canonical QA: continuous validation, recovery, accessibility, mobile compatibility, and explicit evidence.

## Audited from Ima-self-deploy

Deployment/health scripts were audited. Safe concepts are retained as provenance requirements: dependency checks, runtime health checks, build checks, and deployment verification. Environment files, credentials, tokens, and Docker-local deployment state are excluded.

## Audited from Ima-server

The public MCP distribution contract was audited. Its read-only status, learning, distribution, privacy, opt-in, and human-approval boundaries are compatible with the canonical architecture. It remains a distribution/provenance source; the canonical endpoint and runtime remain authoritative.

## Result

One concrete legacy semantic adapter and a reproducible test suite were added to the canonical repository. No second brain, memory authority, feedback authority, or LIVE-001 browser runtime was created.
