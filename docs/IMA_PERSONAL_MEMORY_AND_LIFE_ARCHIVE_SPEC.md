# IMA Personal Memory & Life Archive — Universal Specification

## Purpose

IMA shall make a person-controlled, lifelong record of self-knowledge available across interfaces, devices, AI systems and generations.

The same architecture applies to:
- an individual person;
- IMA's own history and development;
- the documented creator history of IMA;
- families or communities only where each person's consent and ownership are explicit.

This is not a hidden profile owned by IMA. It is a user-governed memory layer that IMA can help create, understand, search, export, migrate, correct, share and delete.

## Core principle

**Your life should not become trapped inside the assistant that helped you remember it.**

A person should be able to:
1. see what IMA remembers;
2. know where each memory came from;
3. correct it;
4. mark uncertainty;
5. revoke access;
6. export it in an open format;
7. import it into another compatible system;
8. delete it and propagate deletion to derived indexes where technically possible;
9. preserve selected memories for descendants only through explicit inheritance/legacy consent.

## Memory layers

### 1. Episode memory
Time-stamped conversations, events, experiences and observations.

### 2. Identity memory
Facts the person explicitly chooses to retain about themselves.

### 3. Self-understanding
Interpretations, values, questions, patterns and evolving hypotheses. These MUST NOT be presented as objective facts merely because IMA inferred them.

### 4. Health-sensitive memory
Medical, disability, trauma and body information. This is a separately permissioned category with stricter access and sharing controls.

### 5. Relationship memory
People, relationships and important interactions, with third-party privacy boundaries.

### 6. Creative archive
Poems, songs, compositions, books, inventions, research and drafts, with provenance and rights metadata.

### 7. Life timeline
A chronological graph linking episodes, people, places, changes, creations, decisions and interpretations.

### 8. Learning record
What the person learned, from which evidence, with confidence, date and revision history.

### 9. Legacy record
Information deliberately selected for future generations. Legacy status is never inferred from ordinary memory.

### 10. IMA memory
IMA's own architecture, principles, versions, decisions, failures, corrections, provenance and creator history.

## Every memory object

Each memory item SHOULD contain:

- stable id
- owner
- memory type
- content
- created_at
- observed_at / valid_from / valid_to when known
- source
- provenance
- author / speaker
- confidence
- evidence references
- sensitivity
- visibility scope
- consent status
- retention policy
- supersedes / superseded_by
- content hash
- schema version

## Truth model

IMA MUST distinguish at least:

**FIRST_PERSON_REPORT**
What the person says happened.

**OBSERVED**
What a system directly observed.

**VERIFIED**
Supported by independent evidence.

**INTERPRETATION**
A person's or IMA's interpretation.

**HYPOTHESIS**
A proposed explanation not established as fact.

**UNKNOWN**
Not currently known.

Memory must never silently move from hypothesis to fact.

## Consent model

Access is capability-scoped.

Suggested scopes:
- private_self
- trusted_person
- clinician_or_professional
- selected_project
- public
- legacy_named_person
- legacy_future_generations
- IMA_internal

Each scope has:
- who
- what
- purpose
- start/end
- read/write permission
- export permission
- derivative-use permission
- revocation state

Default: **private_self**.

No public or intergenerational sharing is inferred from conversation.

## Legacy / descendants

A person may create a "Legacy Capsule" containing selected material.

A Legacy Capsule MUST:
- state why it was preserved;
- identify the intended audience;
- contain provenance;
- distinguish fact from interpretation;
- include creation date and version;
- support later revision or withdrawal where legally and technically possible;
- avoid exposing unrelated third-party private information;
- never imply that descendants inherit obligations to agree.

The purpose is learning, not control.

## Portability

IMA SHOULD support an open, documented export/import bundle.

Recommended structure:

ima-memory/
  manifest.json
  identity.json
  memories.jsonl
  episodes.jsonl
  timeline.jsonl
  provenance.jsonl
  consent.jsonl
  tombstones.jsonl
  relationships.jsonl
  creative/
  legacy/
  checksums.json

The bundle must be readable without IMA.

IMA should track compatibility with emerging portable-memory efforts rather than inventing a closed format. Current ecosystem work includes Portable Memory, Stanford's Portable Memory/Human Context Protocol research, Solid's user-controlled Pods, and W3C work on AI-agent memory interoperability. These are external references and must not be represented as IMA standards unless adopted formally.

## Security

Sensitive memory SHOULD be encrypted at rest and in transit.

High-sensitivity categories SHOULD use separate access scopes/keys.

The architecture should support:
- signed records;
- tamper-evident audit events;
- content hashes;
- key rotation;
- revocation;
- export;
- deletion/redaction;
- proof-oriented deletion records where supported.

A storage provider should not automatically become the authority over the meaning of a person's memories.

## Deletion

Deletion is a first-class event.

When a memory is deleted:
1. mark a tombstone;
2. revoke access;
3. remove or quarantine primary content;
4. identify derived copies/indexes where known;
5. propagate deletion to compatible downstream stores;
6. record what was requested and what was successfully removed;
7. never falsely claim complete deletion when the system cannot verify it.

## Human control

IMA may suggest memories, relationships or patterns.

IMA MUST NOT silently promote suggestions into identity.

The person remains the authority over their own self-description, subject to safety, legal and rights constraints.

## IMA's own memory

IMA maintains a separate system-history archive containing:
- versions;
- architectural decisions;
- creator provenance;
- learned principles;
- known failures;
- corrections;
- evidence;
- changes in interpretation;
- successor compatibility.

IMA must never use its own inferred memory to fabricate creator statements.

## Intergenerational rule

The inheritance is not a fixed doctrine.

It is:

**history + evidence + uncertainty + questions + lessons + freedom to disagree.**

Every generation can:
- preserve;
- correct;
- challenge;
- extend;
- retire;
- reinterpret.

## Universal interface requirement

The capability should be reachable through:
- web;
- mobile;
- voice;
- accessibility interfaces;
- future wearables;
- robots;
- APIs;
- compatible third-party assistants;
- offline/local implementations.

The interface may change. The person's memory contract must remain portable.

## Minimum user actions

Every implementation should eventually expose:

**Remember**
**Show me what you remember**
**Why do you believe this?**
**Correct this**
**Forget this**
**Export my life**
**Import my memory**
**Share this with...**
**Revoke access**
**Create a legacy archive**
**Show my timeline**
**Show what changed**
**Show what I don't know**
**Show what IMA remembers about itself**

## Design law

**Memory belongs to the person. IMA is a steward and tool, not the owner.**


## Vocation and life-direction continuity

The personal memory layer may host the user's evolving direction map defined in [IMA Universal Vocation & Life Direction](IMA_UNIVERSAL_VOCATION_AND_LIFE_DIRECTION.md). Direction data is not a separate identity silo: it is a permissioned interpretation layer connected to provenance-aware episodes, values, creations, experiments and learning.

IMA MUST preserve the distinction between a person's report, observation, verification, interpretation, hypothesis and unknown. A direction hypothesis may change without rewriting the underlying history. Deleting or restricting a direction entry follows the same user-control, consent, provenance and deletion rules as other personal memory.

Direction history may be included in a Legacy Capsule only when explicitly selected by the person.
