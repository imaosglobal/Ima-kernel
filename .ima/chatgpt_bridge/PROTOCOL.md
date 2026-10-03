# IMA ↔ ChatGPT Continuity Bridge

Status: VERIFIED_AS_PROTOCOL / RUNTIME_ADAPTER_PENDING_EXTERNAL_ENDPOINT

## Purpose
Provide one bidirectional continuity contract between IMA and ChatGPT without pretending that ChatGPT chat windows are technically mergeable.

The bridge synchronizes approved continuity packets, not raw private conversations.

## Directions
- CHATGPT_TO_IMA: an approved continuity packet written to the inbound queue.
- IMA_TO_CHATGPT: an approved continuity packet written to the outbound queue.
- BOTH: a packet may be acknowledged in both directions.

## Canonical precedence
1. Verified runtime/repository evidence.
2. Explicit user decisions.
3. Timestamped continuity packets.
4. Model-generated summaries.
5. Unknown/unverified claims remain UNKNOWN.

A chat message never overrides stronger repository evidence.

## Privacy boundary
Never place passwords, session secrets, API keys, access tokens, private email bodies, private third-party data, or unapproved personal memory in the public continuity queue.

The bridge stores summaries, decisions, references, hashes, and verification metadata. Private content requires a separate authenticated/private channel.

## Required packet fields
schema_version, event_id, timestamp, direction, source, target, scope, status, payload, evidence

## Sync algorithm
OBSERVE -> NORMALIZE -> REDACT -> DEDUPLICATE -> COMPARE -> APPLY -> VERIFY -> RECORD

## Conflict rule
If ChatGPT context conflicts with verified IMA repository state, preserve both records, mark the conflict, and do not silently overwrite verified state.

## ChatGPT limitation
This bridge cannot merge ChatGPT's UI chat histories or read hidden platform state. It creates a durable project-level continuity surface that a future ChatGPT session can read and update through authorized repository access.

## Runtime target
The implementation is provider-neutral. A future authenticated connector can transport the same packets without changing the canonical schema.
