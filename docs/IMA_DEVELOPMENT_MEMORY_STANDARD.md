# IMA Development Memory Standard

## Purpose

IMA records meaningful development as dated, provenance-aware memory rather than relying only on source-code snapshots.

## Required fields

Every development event SHOULD contain:

- `timestamp`: ISO-8601 timestamp with timezone.
- `event`: stable event category.
- `summary`: concise description of what happened.
- `source`: component, tool, person, or process that produced the record.
- `status`: verification state such as `RECORDED`, `VERIFIED`, or `GAPS_RECORDED`.
- `details`: structured evidence, identifiers, changes, limitations, and follow-up checks.

## Layers

1. **Runtime journal** — `.ima/journal/development.jsonl` for chronological events.
2. **Component journals** — reflection/worldview/runtime state files for domain-specific records.
3. **Git history** — durable history of code and documentation changes.
4. **External provenance** — provider/tool identifiers and returned evidence when available.

## Rules

- Never silently rewrite historical events.
- Never mark an event verified without evidence.
- Never claim a provider, person, source, or tool was consulted when it was not.
- Preserve uncertainty and failed checks as part of the memory.
- Distinguish planned, attempted, executed, verified, and failed work.
- Keep timestamps timezone-aware.
- Treat memory as auditable state, not as proof of truth.
- Future components should append to the journal instead of replacing it.

## Continuity

The development journal is part of IMA's Future Continuity Contract. New capabilities should integrate their significant state transitions with this standard so that IMA can reconstruct what changed, when it changed, why it changed, what evidence supported it, and what remained unresolved.
