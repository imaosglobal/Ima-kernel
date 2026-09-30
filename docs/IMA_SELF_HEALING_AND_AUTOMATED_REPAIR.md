# IMA Self-Healing and Automated Repair

## Purpose

IMA must not stop at detection.

The permanent operations loop is:

DETECT -> DIAGNOSE -> CLASSIFY -> REPAIR -> TEST -> VERIFY -> REPORT -> OBSERVE

A repair is only considered successful when the affected verification layer passes again.

## Current repair: continuity runtime bootstrap

The canonical runtime previously failed on a fresh CI checkout with:

CONTINUITY_SEEDS_NOT_FOUND

The continuity files are mutable runtime state, not source-code secrets. They are intentionally not required to be present in a clean clone.

The portable identity layer now repairs the valid empty-state case automatically:

1. Creates .ima/runtime/continuity/ when absent.
2. Creates an empty knowledge_seeds.jsonl when no continuity state exists.
3. Creates an empty content_address_index.json with an explicit schema and zero records.
4. Builds a deterministic empty portable identity index.
5. Verifies the resulting state.
6. Does not invent content, hashes, provenance, identities, or user data.

This distinction is important:

- Missing mutable state on a fresh installation is repairable.
- A referenced artifact whose content is missing is not fabricated; the runtime still fails with CONTENT_OBJECT_NOT_FOUND:<artifact_id>.
- A hash mismatch remains an integrity error.
- Existing non-empty continuity state is never silently overwritten.

## Repair contract

Every future self-repair must:

- be deterministic;
- preserve provenance;
- never fabricate facts or content;
- never overwrite originals;
- remain within IMA policy and authorization boundaries;
- emit an observable result;
- run the relevant tests after repair;
- provide a rollback/disable path for consequential changes.

## Continuous health

The continuous health workflow is the enforcement layer. It must verify both detection and repair behavior.

A green run means the tested repair path and all subsequent checks completed successfully; it does not mean that every possible production failure is impossible.

## Product operations

For each recurring failure class, IMA should maintain:

- failure signature;
- owner/component;
- diagnosis method;
- safe repair procedure;
- verification test;
- observability signal;
- provenance;
- rollback/disable procedure;
- current status.

This turns the health system from a logger into a bounded, testable self-maintenance system.
