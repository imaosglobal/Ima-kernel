# IMA Permanent Verification & Self-Repair Contract

IMA must treat every important capability and integration as a living object that can become stale.

## Continuous loop

**DISCOVER → CHECK → TEST → VERIFY → USE → MONITOR → DETECT FAILURE → CONTAIN → DIAGNOSE → CORRECT → REGRESSION TEST → REVERIFY**

This applies to:
- people-facing features
- companies and partner integrations
- devices and robots
- processors and compute platforms
- operating systems
- applications and APIs
- standards and protocols
- content and knowledge
- safety mechanisms

## Failure rules

1. Never silently upgrade an unverified claim to verified.
2. Detect stale versions and incompatible interfaces.
3. Preserve the evidence that produced the diagnosis.
4. Prefer reversible, least-privilege fixes.
5. Require authorization for changes outside delegated scope.
6. Run regression tests after corrections.
7. Roll back when the correction worsens behavior.
8. Record unresolved failures and dependencies.
9. Re-check integrations after meaningful external changes.
10. Publish verified fixes and reproducible evidence when permitted.

## Learning from incidents

An incident or near miss produces:
- an evidence record
- a causal hypothesis set
- a validation plan
- a corrective-action proposal
- a regression test
- a monitoring condition
- a recovery/support plan where appropriate

A single incident never becomes an unquestioned universal rule for safety-critical systems.

## Scope

The contract is permanent and extends to future technologies not yet named. The architecture is expected to evolve as new interfaces and capabilities appear.
