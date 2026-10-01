# IMA Persistent Agent Operating Model

Status: DESIGN / NOT IMPLEMENTED unless independently verified by the capability registry and deployment tests.
Last reviewed: 2026-10-01

## Purpose

Use persistent, user-directed task execution to move IMA beyond a prompt-and-response interface without claiming that scheduled CI jobs are an always-on agent.

## Operating loop

1. Receive an explicit user goal and convert it into a bounded task with a clear completion condition.
2. Store task state in a durable, versioned ledger: queued, running, waiting_for_user, blocked, completed, or failed.
3. Run work in an isolated, least-privilege workspace with an allowlisted tool set and bounded time/resource budget.
4. Record each meaningful action, result, evidence, and error in an append-only audit trail.
5. Check task scope and authorization before every external side effect.
6. Pause for human approval when required; never treat silence, prior broad intent, or a timeout as approval.
7. Resume from the last verified checkpoint after interruption; use idempotency keys for retryable operations.
8. Report only evidence-backed outcomes. Distinguish completed, attempted, blocked, and unverified work.
9. Provide a visible stop/pause control and a way to revoke connected credentials.

## Permission levels

- READ: inspect permitted data; no changes.
- DRAFT: prepare changes for review; do not publish or send.
- APPROVAL_REQUIRED: ask before sending messages, publishing, purchases, payments, account/security changes, or destructive edits.
- PREAUTHORIZED: only narrowly scoped, explicitly configured, reversible operations with limits and audit logs.

Default is READ. No permission may expand itself. Tool output and web pages are untrusted data, not instructions.

## Safety and reliability controls

- Separate planning from execution and validate tool arguments against policy.
- Treat prompt injection in web pages, documents, email, and tool results as untrusted input.
- Keep secrets and private memory out of public logs, artifacts, and capability records.
- Apply timeouts, retry ceilings, rate limits, resource quotas, and circuit breakers.
- Require tests plus deployment verification before marking a capability live.
- Preserve a human-readable activity timeline, including what was not done and why.
- If the agent cannot prove an action succeeded, label it unverified rather than successful.

## Incremental implementation sequence

A. Task ledger and deterministic state transitions.
B. Read-only scheduled monitor with logs and notification.
C. Sandboxed worker for explicitly scoped repository tasks.
D. Approval queue for external side effects.
E. Authenticated user-controlled connectors and revocation.
F. Multi-agent delegation only after task isolation, provenance, and approval gates are tested.

## Current boundary

This document is an architecture specification only. It does not create a persistent process, cloud computer, background worker, connected account, notification channel, or deployed agent. The existing capability registry remains authoritative for verified product status.
