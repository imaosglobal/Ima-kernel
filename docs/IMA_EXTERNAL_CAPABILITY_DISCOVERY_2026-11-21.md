# IMA External Capability Discovery — 2026-11-21

The daily unified audit now includes an external capability-discovery stage.

## Discovery scope
- GitHub repositories and source projects
- MCP/App standards
- browser/computer-use ecosystems
- human-in-the-loop and approval patterns
- memory/provenance systems
- agent security and red-team practices
- future company, startup, hardware and software sources when evidence is available

## Required sequence
Observe → identify candidate → deduplicate → conflict-check → security/privacy check → evidence check → adapt to IMA contracts → test → deploy only through the canonical pipeline → runtime verify → document.

## Non-negotiable boundaries
- No second brain, memory authority, feedback authority or LIVE-001 runtime.
- No secrets, credentials or private data imported from external projects.
- No autonomous consequential action.
- No promotion from source claims to live capability without reproducible evidence.
- Existing IMA principles and governance take precedence over imported implementation patterns.

## Today
Four external patterns were integrated as canonical, evidence-bounded contracts:
- accessibility-tree action mapping
- human approval contract
- memory provenance/correction/withdrawal
- agent security regression checks

They are recorded as IMPLEMENTED_IN_CODE / TESTED_PENDING_CI.

The scheduled workflow now runs the discovery contract daily and persists a candidate ledger for canonical review.
