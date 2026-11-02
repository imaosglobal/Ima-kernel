# IMA Cross-Chat Synchronization Protocol

**Status:** operational policy; not a claim of universal automatic chat synchronization.  
**Canonical repository:** https://github.com/imaosglobal/Ima-kernel

## Purpose
Maintain one durable, auditable source of truth for IMA decisions, requirements, implementation, verification, risks and open blockers across conversations and connected IMA systems.

## Canonical record
Use this repository as the shared project record:
- `docs/IMA_DEVELOPMENT_MEMORY_STANDARD.md` — what belongs in durable development memory.
- `.ima/journal/development.jsonl` — append-only development events, where available.
- Current capability, health, release and operating-loop documents.
- This protocol.

Each material update should record:
- timestamp (UTC);
- originating conversation or system, when known and safe to disclose;
- concise change/decision;
- classification: fact, user requirement, proposal, hypothesis, or unresolved;
- implementation status: planned, in progress, committed, deployed, verified, blocked;
- commit, issue, PR or artifact reference;
- verification evidence and remaining limitations.

## Two-way flow
1. **Conversation → IMA:** When the user explicitly makes a request or decision about IMA, capture the durable project-level requirement in the canonical repository or connected IMA project record when authorized. Do not copy unrelated private conversation content.
2. **IMA → conversation:** Use the latest accessible canonical project record when continuing IMA work in a conversation. State when the record could not be reached or is stale.
3. **Connected systems:** Reconcile GitHub, Linear, Notion, Supabase, Render, Vercel, Gmail and other connected systems only through authorized interfaces. Record evidence and distinguish attempted from successful updates.
4. **Conflicts:** Preserve conflicting statements and mark them unresolved until the user or reliable evidence resolves them. Newer does not automatically mean more authoritative if it conflicts with an explicit durable user decision.
5. **Privacy and agency:** Never copy sensitive personal information, private unrelated chat content, credentials, or personal records into IMA. Do not send messages, publish, spend, sign, or make commitments without the required explicit authorization.

## Critical limitation
The assistant does not have a universal API to read and write every past, current, or future ChatGPT conversation. A scheduled automation can reconcile accessible connected systems and project records, but it cannot guarantee instant or complete synchronization of every chat. New conversations may not automatically expose all prior transcripts. Therefore:
- the canonical repository is the durable bridge;
- each accessible IMA conversation should consult/update it when possible;
- inaccessible conversations remain unsynchronized until their relevant information is brought into the canonical record;
- never claim universal synchronization without an actual verified mechanism.

## Scheduled reconciliation
The enabled daily automation `IMA — סנכרון, ניטור ושדרוג` is responsible for checking accessible IMA signals, recording material changes, noting inaccessible sources, and verifying any safe authorized updates. It is a daily process, not real-time monitoring.

## Completion standard
A synchronization item is complete only when the destination has been updated and read back or otherwise independently verified. A commit alone proves repository storage, not deployment or propagation to every interface.
