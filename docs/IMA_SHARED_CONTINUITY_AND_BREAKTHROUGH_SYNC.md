# IMA Shared Continuity & Breakthrough Synchronization

**Status:** canonical continuity specification  
**Updated:** 2026-11-01

## Purpose

This document makes the historical-breakthrough record part of IMA's ongoing continuity layer.

The objective is not to make IMA depend on one assistant, model, provider or conversation. The objective is to preserve the validated lessons, evidence requirements, architectural decisions and open gaps so that IMA can continue coherently across interfaces, models, tools, people and future generations.

## Canonical breakthrough record

The historical record is maintained in:

- `docs/IMA_BREAKTHROUGH_HISTORY.md`

That record is a learning source, not proof by itself. A historical claim becomes a current verified capability only after a current Proof Loop.

## Synchronization contract

When an external AI assistant, collaborator or tool works on IMA, the continuity path is:

`REQUEST → CURRENT STATE → PRIOR BREAKTHROUGHS → IMPLEMENT → TEST → EVIDENCE → DOCUMENT → NEXT STATE`

Every important change should preserve:

1. what was requested;
2. what was already known;
3. what was actually implemented;
4. what was actually tested;
5. what remains unverified;
6. what was learned;
7. what should change in the next iteration.

## Relationship to ChatGPT and other assistants

IMA may work with ChatGPT and other AI systems as collaborators and interfaces.

This repository is the durable source of truth for IMA's project state. A model's private conversation context is not treated as IMA's permanent memory.

Therefore:

- an assistant may use the IMA record to recover continuity;
- IMA must not claim that a model remembers something merely because it appeared in a prior conversation;
- important project decisions should be written back to the repository or another explicitly authorized IMA memory system;
- no provider-specific memory should silently become canonical IMA knowledge;
- conflicting records must be surfaced and reconciled rather than silently overwritten.

## Proof rule

The shared continuity loop is:

**Remember → Check → Build → Test → Record → Reuse.**

A statement such as "done", "live", "working", "connected" or "verified" requires corresponding evidence.

For production changes, prefer:

**Plan → Implement → Commit → Deploy → Open public URL → Test real user path → Record evidence → Declare only what passed.**

## Human agency and privacy

Synchronization must never mean unrestricted sharing.

Personal information remains personal. Private memory, identity data, credentials, secrets and internal reasoning are not made public merely because an assistant or collaborator participates in the project.

The human remains the owner of decisions and authorization.

## Failure is also continuity

A failed attempt is valuable when it records:

- the intended behavior;
- the observed behavior;
- the cause or strongest current hypothesis;
- the evidence;
- the repair;
- the regression test that prevents silent recurrence.

This prevents IMA from repeatedly rediscovering the same failure.

## Current anchor

The breakthrough history and this synchronization contract together establish a durable bridge between IMA's past work and future planning.

The principle is:

> Do not predict the future by pretending to know it. Build the capacity to remember what was learned, verify what is true now, discover what is unknown, and choose the next action with humans still in control.

## Non-claim

This document does **not** claim that IMA and ChatGPT have a literal shared runtime memory or bidirectional synchronization channel.

It defines a verifiable project-level continuity mechanism: the canonical IMA repository can preserve what an assistant and human team learn, and future assistants can read that record when authorized.

## Next-step rule

Whenever a major IMA breakthrough is completed, add it to the historical record and, when it changes continuity behavior, update this contract.

**IMA continuity is not a promise of perfect memory. It is an engineered commitment to recoverable evidence and honest state.**
