# IMA Unified Process Architecture

Status: PROPOSED — design and implementation contract; not a claim that all workflows are already unified.

## Objective
Give every existing and future IMA process one shared lifecycle, identity, observability, and safety contract while keeping specialized workers independently deployable. Unification means one control plane and common interfaces, not one giant workflow or unrestricted autonomous execution.

## Control plane
The canonical process registry is the source of truth. Each process must declare:
- stable `process_id`, owner, purpose, version, enabled state;
- trigger (schedule, event, manual, request), inputs and output schema;
- dependencies, timeout, retry/backoff, idempotency key and concurrency group;
- required permissions, data classification, network/provider scope;
- risk tier, approval gate, rollback/compensation, health check;
- evidence location, retention, last successful run and failure state.

## Shared lifecycle
`DISCOVERED → REGISTERED → VALIDATED → APPROVED (when required) → READY → RUNNING → VERIFIED → COMPLETED`.
Failures transition to `RETRY_PENDING`, `BLOCKED`, or `FAILED`; destructive or externally consequential work requires explicit authorization. Never mark VERIFIED without test or runtime evidence.

## Common event envelope
Use versioned JSON events with `event_id`, `process_id`, `process_version`, `occurred_at` (UTC ISO-8601), `correlation_id`, `trigger`, `status`, `input_digest`, `output_digest`, `evidence_refs`, and `error_code`. Avoid storing secrets or raw personal data in logs. Journal is append-only; corrections are new events.

## Integration rules
1. Inventory workflows, cron jobs, daemons, API handlers, app actions, agents, and external integrations; assign stable IDs and owners.
2. Adapt each process through a thin adapter to the common event/lifecycle contract; preserve its specialized implementation.
3. Route schedules/events through the orchestrator/registry; avoid duplicate schedulers and overlapping writes.
4. Require idempotency, bounded retries, timeouts, cancellation, rate limits, and dead-letter/failure visibility.
5. Separate discovery from installation, activation, deployment, purchases, messages, and other external side effects.
6. Capability radar findings remain unreviewed until fit, safety, privacy, licensing, security, and tests pass.
7. Use least privilege and scoped credentials; never forward user data to external AI providers without a declared purpose and authorization.
8. Keep human approval for high-impact changes; no self-approval, silent permission expansion, or automatic merging.
9. Every process must expose health, last run, next run where applicable, duration, outcome, and evidence.
10. New processes cannot enter production unless they satisfy this contract and have an owner, tests, rollback, and monitoring.

## Phased implementation
- Phase A: inventory and registry; classify all current workflows/services and identify duplicate triggers.
- Phase B: shared event schema, journal writer, run IDs, health dashboard and failure routing.
- Phase C: adapters for low-risk read-only jobs, then tests and reversible maintenance.
- Phase D: migrate deployment, payments, user communications, data mutation and AI-provider actions only behind explicit approval gates.
- Phase E: enforce registry validation in CI; reject unregistered workflows/processes.

## Acceptance criteria
- Every active process is catalogued and has a stable ID.
- No process has overlapping uncontrolled writers or duplicate schedules.
- Each run is traceable from trigger through result and evidence.
- Failed, skipped, stale, and blocked states are distinguishable.
- New process PRs fail CI if required metadata/tests/permissions are missing.
- Rollback and approval behavior is tested for consequential actions.

## Current implementation boundary
This document defines the target architecture. It does not itself migrate existing workflows, start a daemon, or prove runtime operation. Migration is complete only when inventory, adapters, CI enforcement, and live run evidence are present.


## Implemented in this change
Phase A is now represented by the canonical `.ima/process_registry.json`. Phase E has an initial CI enforcement workflow at `.github/workflows/ima-process-registry.yml`, backed by `scripts/ima_process_registry_validate.py`. These additions validate the registry itself; they do not yet prove that every historical workflow, daemon, API handler, agent, or external integration has been migrated into it.
