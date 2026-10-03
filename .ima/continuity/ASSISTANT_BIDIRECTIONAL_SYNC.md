# IMA ↔ External Assistant Bidirectional Continuity

Status: protocol specification.

Purpose: maintain a durable, evidence-based handoff between IMA and the assistant sessions used to operate it.

Directions:
- ASSISTANT_TO_IMA: approved context, decisions, evidence and requested changes are handed into IMA.
- IMA_TO_ASSISTANT: verified IMA state, decisions, evidence and open gaps are handed to the next assistant session.

Rules:
1. Repository evidence outranks model summaries.
2. Unknown remains unknown.
3. Never store passwords, tokens, secrets or raw private conversations in the public repository.
4. Every packet has a timestamp, source, target, status and evidence reference.
5. Duplicate packets are ignored by stable event id.
6. Conflicts are preserved and marked rather than silently overwritten.
7. This synchronizes project continuity; it does not claim access to hidden platform conversation history.

Loop:
OBSERVE -> NORMALIZE -> REDACT -> DEDUPLICATE -> COMPARE -> APPLY -> VERIFY -> RECORD
