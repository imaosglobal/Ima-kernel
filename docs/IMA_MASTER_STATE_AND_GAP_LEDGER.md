# IMA Master State & Gap Ledger

**Status:** canonical audit/reconciliation layer  
**Audit date:** 2026-10-30  
**Scope:** historical IMA direction recovered from available conversation context + current GitHub repository evidence + connected-tool state that was actually inspectable in this audit.  
**Truth rule:** conversation intent, documentation and source code are evidence of intent/implementation; they are not proof of deployed or live behavior.

## 1. State model

Every work item must use exactly one primary state:
- VERIFIED_LIVE — real deployed behavior independently exercised and evidenced.
- DEPLOYED_PENDING_LIVE — deployment evidence exists, live behavior still needs exercise.
- TESTED_PENDING_DEPLOYMENT — reproducible tests exist, deployment not proven.
- IMPLEMENTED_IN_CODE — implementation exists; required tests/deployment/live evidence incomplete.
- DESIGNED — architecture/spec exists; implementation incomplete.
- PLANNED — requirement/backlog only.
- BLOCKED — a concrete prerequisite prevents progress.
- SUPERSEDED — replaced by a canonical newer implementation.
- DUPLICATE — redundant work item; preserve reference, do not build another system.

## 2. Canonical control plane

| Area | State | Evidence | Main gap / next action |
|---|---|---|---|
| Master requirements ledger | IMPLEMENTED_IN_CODE | docs/IMA_MASTER_REQUIREMENTS_LEDGER.md | Keep synchronized with every new request |
| Continuous evolution contract | IMPLEMENTED_IN_CODE | docs/IMA_CONTINUOUS_EVOLUTION_CONTRACT.md | Runtime evidence remains required |
| Capability registry | IMPLEMENTED_IN_CODE | docs/IMA_CAPABILITY_REGISTRY.json | Expand evidence fields and reconcile stale statuses |
| Unified daily loop | IMPLEMENTED_IN_CODE | .ima/loop/unified_loop.py + .github/workflows/ima-unified-loop.yml | Obtain a fresh successful workflow run after current fixes |
| Public reconciliation | IMPLEMENTED_IN_CODE | scripts/ima_public_reconciliation.py | Browser/API/deployment verification still required |
| Multi-perspective review | IMPLEMENTED_IN_CODE | workflow + .ima/multi_perspective | Make findings actionable rather than only writing a matrix |
| World-model monitor | IMPLEMENTED_IN_CODE | scripts/ima_world_model_availability_check.py | Authorized provider access + bounded live request |
| Development evidence journal | IMPLEMENTED_IN_CODE | .ima/journal + loop state | Ensure all historical work items converge here |

## 3. Highest-risk unresolved product gates

### P0 — Public chat normal response
State: DEPLOYED_PENDING_LIVE / blocker.  
Evidence: GitHub issue #106 reports a real public browser request reached the deployment but exposed an internal runtime fallback exception.  
Required: identify exact runtime path, fix data-shape error, suppress internal exception from users, production smoke test, redeploy, cache-busted browser test, record evidence.

### P0 — Canonical unified-loop health
State: BLOCKED_FOR_VERIFICATION.  
Evidence: open failure issues #121 and #114 exist; later code fixes were committed, including fed606b..., but a fresh successful run after the fixes is not currently verified through the available GitHub connector.  
Required: obtain a new run/result and inspect logs before declaring the loop healthy.

### P1 — Google authentication
State: IMPLEMENTED_IN_CODE / RUNTIME_CONFIGURATION_GAP.  
Evidence: master ledger AUTH-001; app.py contains Google token verification path.  
Required: real Google OAuth client/origin configuration, canonical Render environment configuration, real browser login/session/logout/chat authorization, Android Credential Manager and cross-device verification.

### P1 — Universal memory
State: IMPLEMENTED_IN_CODE / DEPLOYED_PENDING_RUNTIME.  
Evidence: .ima/ima_canonical_memory_adapter.py now delegates to canonical universal memory; tests and app endpoints exist.  
Risk: legacy conversation_layer.py still contains a separate JSON conversation store. It must be reconciled so it cannot become a parallel canonical memory system.  
Required: one runtime memory path, consent/isolation/export/correction/deletion/retention tests, live verification.

### P1 — Child safety
State: IMPLEMENTED_IN_CODE / RUNTIME_AND_INDEPENDENT_REVIEW_REQUIRED.  
Evidence: issue #110 records first-pass screening, response enforcement and regression tests.  
Required: route-level/live tests, multilingual and age-banded evaluation, red-team review, independent child-safety review, shared enforcement boundary, caregiver/educator co-design, legal/jurisdiction review before broad child rollout.

### P1 — Public UX
State: IN_PROGRESS.  
Evidence: public reconciliation checks source presence for Google login, chat, memory controls, accessibility, RTL, community, shop, media and PWA.  
Required: real browser matrix across supported controls, auth states, mobile, loading/error/fallback paths.

## 4. Major capability families

### Human-centered intelligence
State: IMPLEMENTED_IN_CODE / TESTED_PENDING_LIVE.  
Human-intelligence charter, provider-neutral policy and regression tests exist. Gap: all active runtime entry points still need behavioral verification.

### Human culture
State: IMPLEMENTED_IN_CODE / TESTED_PENDING_LIVE.  
Executable culture policy and tests exist. Gap: production behavior and multilingual coverage.

### Peace / dignity / de-escalation
State: IMPLEMENTED_IN_CODE / TESTED_PENDING_LIVE or NOT_VERIFIED depending on capability.  
Policy, peace layer and tests exist. Gap: live deployment, outcome measurement, multilingual/high-stakes validation.

### Intergenerational memory / preservation
State: IMPLEMENTED_IN_DOCUMENTATION / RUNTIME_INTEGRATION_REQUIRED.  
Charters and preservation architecture exist. Gap: verified runtime capture, provenance, correction, export and deletion.

### Creator questions / inner voice / vocation / backward reflection
State: DOCUMENTED / RUNTIME_PARTIAL.  
Canonical charters exist. Gap: map each framework to actual runtime behavior and tests without turning reflection frameworks into deterministic psychological claims.

### Social physics / observer-relative methodology
State: RESEARCH_PROGRAM / IMPLEMENTED_IN_CODE.  
Research framework, methodology and restored Python source exist. Gap: empirical validation, falsification, replication; never promote hypotheses as physical law.

### World models / Genie
State: ACCESS_REQUIRED.  
Provider-neutral safety bridge, contract, tests and official availability monitor exist. Gap: authorized provider access and successful bounded real generation request.

### Device continuity
State: IMPLEMENTED_IN_CODE / DEPLOYED_PENDING_DEVICE_REPORT.  
Web/PWA health bridge and identity architecture exist. Gap: authenticated cross-device runtime proof and device-specific evidence.

### 3D presence / avatar
State: IMPLEMENTED_IN_CODE / DEPLOYED_PENDING_RUNTIME.  
GLB and continuity docs exist. Gap: browser/runtime integrity and truthful fallback verification.

### Voice / vision
State: NOT_VERIFIED.  
Browser TTS exists; live bidirectional voice/vision is not verified. Gap: provider-backed runtime and device matrix.

### Image/video generation
State: NOT_VERIFIED.  
Architecture/media references exist. Gap: live public generation provider and runtime proof.

### Community
State: IMPLEMENTED_IN_CODE / RUNTIME_PARTIAL.  
UI and architecture references exist. Gap: real user flows, moderation, reporting, privacy and adoption evidence.

### Store / payments
State: DISABLED.  
Catalog exists; automatic checkout/spending is intentionally not enabled. Gap: only enable after explicit lawful payment architecture and human authorization controls.

### Growth / Trend-to-Brand
State: IMPLEMENTED_IN_CODE / TESTED_PENDING_LIVE.  
Issue #108 and continuous-evolution contract define the pipeline. Gap: evidence-backed live discovery, validation, economics and authorized pilots.

### Universal interoperability / external integrations
State: DESIGNED / PARTIAL.  
Issues #118, #119 and #122 define the adoption program and safety boundaries. Gap: real external authorization, adapters, conformance tests and reproducible independent integrations.

### Distribution / public discovery
State: IMPLEMENTED_IN_CODE / DEPLOYED_PENDING_VERIFICATION.  
Universal distribution protocol and ChatGPT discovery metadata exist. Gap: verified public distribution, search discovery and real-user activation evidence.

### Revenue / nonprofit / creator separation
State: GOVERNANCE_IMPLEMENTED / LEGAL_STATUS_PENDING.  
Financial schema, nonprofit charter and succession framework exist. Gap: no legal nonprofit registration is claimed; real financial events require evidence; personal creator rights remain separate.

## 5. Historical technical debt recovered from earlier work

- Old ima_learning service was previously down because it referenced missing ima_one_brain.py; canonical memory boundaries and action deduplication were subsequently developed. Current status must be checked against present architecture rather than assuming the old service is still canonical.
- Many archived snapshot directories existed historically; canonical single-snapshot authority was established. Future work must not revive parallel snapshot authorities.
- A prior conversation_layer.py JSON store remains in the repository; this is now a reconciliation target, not a second memory architecture.
- A prior malformed CapabilityFactoryTests issue is no longer present in the current fetched file; the current test class is syntactically normal. Historical issue text must not be treated as current code truth.
- save_memory in the canonical adapter is no longer a no-op; it delegates to the canonical universal memory runtime. Historical issue text is therefore stale on that point.
- Social-physics source syntax was repaired on 2026-10-29.
- Self-worth test import was repaired on 2026-10-29.
- Canonical CI test discovery was changed to include repository package root on 2026-10-29.
- World-model humanization, provider contract, evolution policy and availability monitoring were added on 2026-10-30.

## 6. Open GitHub programs that must converge into this ledger

- #106 — public chat fallback blocker.
- #107 — Universal Conversation & Interaction Memory.
- #108 — Trend-to-Brand Engine.
- #109 — human-understanding behavior across interfaces.
- #110 — intergenerational/global rollout and child-first safeguards.
- #118 — universal interoperability & safety network.
- #119 — global adoption and real integrations.
- #121 / #114 — unified-loop failures; must be reconciled against fresh runtime evidence.
- #122 — verified external connections.

These are workstreams, not separate schedulers.

## 7. Historical idea-to-state rule

For every new idea from conversation, email, repository, external research or future user request:

CAPTURE → DEDUPE → REQUIREMENT_ID → CLASSIFY → LINK_TO_CANONICAL_SYSTEM → IMPLEMENT → TEST → DEPLOY → VERIFY_LIVE → DOCUMENT → TEACH/CARRY_FORWARD

If implementation already exists, update it rather than create a duplicate.

If only the idea exists, it remains PLANNED or DESIGNED.

If a prerequisite is unavailable, record BLOCKED with the exact prerequisite.

If evidence is stale, downgrade the claim rather than preserve an optimistic status.

## 8. Future request ingestion

New user proposals are not lost in chat. The canonical loop must:
1. create/reuse a stable work-item ID;
2. search for semantic duplicates;
3. link to code/docs/issues;
4. classify implementation/test/deployment/live evidence independently;
5. prioritize P0/P1 blockers and user-visible failures;
6. execute safe authorized work;
7. record exact evidence;
8. carry incomplete work forward;
9. close or supersede obsolete items without deleting provenance.

## 9. Immediate execution order

1. Public chat P0.
2. Fresh canonical-loop CI evidence.
3. Google authentication runtime configuration/verification.
4. Canonical memory consolidation and runtime verification.
5. Public browser/mobile UX matrix.
6. Child-safety shared enforcement + independent review gate.
7. Device/cross-device verification.
8. External integration conformance framework.
9. World-model provider access and bounded live test when authorized.
10. Growth/distribution measurement and real-user evidence.
11. Research capabilities: empirical validation before promotion.
12. Continuous future-capability intake through this same ledger.

No item is allowed to disappear merely because it was discussed months earlier.
