# IMA Feedback Ledger & Execution Contract

## Purpose
Every feedback item must have one durable canonical record, provenance, learning result, execution state, evidence, and unresolved work.

## Canonical lifecycle
1. Receive immediately.
2. Persist durably in Supabase `public.feedback_archive`.
3. Preserve source/channel, auth state, page/referrer, client time/timezone, user agent, and structured metadata.
4. Classify into a learning category and priority.
5. Record a learning action.
6. Execute the learning-ingest step automatically.
7. Create a separate product-change candidate.
8. Product changes are applied only after verification and tests; external/public side effects remain approval-gated.
9. Record evidence and applied timestamp.
10. Re-evaluate recurring feedback in the daily rollup.

## Status meanings
- `applied`: the learning/operational step actually ran and evidence was recorded.
- `proposed`: a product/system change is identified but not yet proven/applied.
- `failed`: an attempted action failed and requires retry/investigation.
- `needs_review`: the action cannot be safely automated with current verified capabilities.

## Current channels
The canonical feedback API accepts: `public-runtime`, `ima-chat`, `ima-app`, `meta`, `whatsapp`, `telegram`, `email`, `api`.
A channel is not considered connected merely because the value is accepted; the channel must have a verified ingestion path before it is reported as active.

## Privacy
Feedback records use privacy-preserving identity labels. Raw email/name is not stored by the feedback endpoint. Historical records without a sender are labeled `לא מתועד`. Raw personal chat content must not be exposed to other users.

## Historical evidence
Legacy learning/action evidence is preserved in `public.feedback_legacy_evidence` and surfaced through `ima_internal.feedback_ledger`. It is explicitly marked as legacy evidence rather than being represented as a new user feedback submission.

## Executor boundary
The executor automatically applies the learning-ingest stage and records evidence. It does not silently modify arbitrary source code, publish externally, contact people, spend money, or change third-party accounts. Such changes become product-change candidates and require verified implementation paths and tests.

## Recurring automation
Supabase Cron runs:
- near-real-time learning: every minute
- feedback executor: every minute
- daily rollup: daily at 00:05 UTC

## Reporting
The canonical report source is `ima_internal.feedback_ledger` plus `public.feedback_execution_log` and `public.feedback_daily_rollup`. Future requests for “all feedback” should read these sources and explicitly separate:
- canonical user feedback
- legacy learning/action evidence
- learned lessons
- applied changes
- proposed changes
- unresolved blockers
