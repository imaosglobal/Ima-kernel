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

## 2026-10-30 daily reconciliation update

- **PUBLIC-DEPLOY-001 — canonical Pages reconciliation:** current `gh-pages/index.html` was materially older/different from the canonical `ima-ui` source. A native GitHub Actions build-and-publish workflow was added at `.github/workflows/deploy-ima-pages.yml` (commit `b0ff277ca04786c86aa04bec6a7694f71a15dd89`). State: **EXECUTED / DEPLOYMENT_PENDING_VERIFICATION**.
- **LOOP-JOURNAL-001 — development memory continuity:** the canonical unified loop now appends task-level and cycle-level state transitions to `.ima/journal/development.jsonl` (commit `eae744916b50eae633995092648e8e8f18844e00`). State: **IMPLEMENTED_IN_CODE / FRESH_RUNTIME_VERIFICATION_PENDING**.
- **GROWTH-002 — self-marketing capability registry:** self-marketing/sales/brand/growth is explicitly registered as a first-class capability, evidence-bounded and not live-promoted without runtime analytics/evidence (commit `4492ce75ab959232e51f596a81567f19993bf624`). State: **IMPLEMENTED_IN_CODE / TESTED_PENDING_LIVE**.
- **CI-VERIFY-001:** historical failed workflow runs remain historical evidence only; no current successful canonical run was available through the connected GitHub workflow-run surface in this cycle. State: **NOT_VERIFIED**.

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


## 10. Technology frontier and IP execution

- Added `docs/IMA_TECHNOLOGY_FRONTIER_RADAR.md` as the canonical technology-intake and integration policy across 20 frontier domains.
- Added `docs/IMA_INVENTION_DISCLOSURE_AND_IP_PIPELINE.md` with four invention candidates, prior-art warnings, human-inventorship/legal gates, and a revenue-ledger design.
- Initial 2026 prior-art review found substantial existing patent activity around agent orchestration, approval-bound execution, provenance, AI lineage, consent-aware personalization and multi-agent consent. Therefore IMA will not label any candidate a patent or claim novelty until a dated invention disclosure, human contribution record, claim chart and professional review exist.
- Economic rule: potential royalties may be recorded only after actual licensing and payment evidence. The target allocation model is mission + creator + community/user benefit, subject to ratified governance and law.

## 11. 2026-10-30 execution delta

### Public chat P0
- **Fix committed:** `c6c4fb41d332cdd3705a823f8e478c0b4a330862`.
- The master runtime now isolates provider, knowledge-graph, brain and private-memory answer paths.
- Malformed knowledge/provider data can no longer be returned as the public response.
- Internal exceptions are retained only in runtime diagnostics; a bounded safe answer is returned instead.
- **Regression test committed:** `0b1751c5cd344b73e926a61880dc5fe45c8a02e` — verifies the previously reported list-index shape error cannot leak to the user.
- **State remains:** TESTED_PENDING_DEPLOYMENT until a fresh deployed/browser request proves a normal response.

### Canonical memory consolidation
- **Compatibility fix committed:** `9fe03cae798b911aa0fc4d3f2009c1878783c7f4`.
- `conversation_layer.py` no longer owns a JSON conversation store; it delegates its historical API to the canonical universal interaction-memory runtime.
- This removes a known parallel persistence authority while preserving existing callers.
- **State:** IMPLEMENTED_IN_CODE / TESTED_PENDING_DEPLOYMENT; live consent/isolation/export/deletion verification remains required.

### Verification boundary
These commits are implementation evidence only. No deployment or live-public success is declared until a fresh runtime/browser test produces independently inspectable evidence.


### Canonical memory regression coverage
- **Regression test added:** `6b32c1e47ef14e4b751af92527dcd1f0ed66fe83`.
- Covers explicit consent gating, per-user isolation, integrity verification, deletion, and rejection of credential-like content.
- **State:** TESTED_PENDING_DEPLOYMENT; this is repository-level evidence, not live deployment proof.


## 2026-11-03 — Dynamic identity and movement integration

- **Source:** Ori Cohen's poem and inquiry, "תנועות", and the follow-up instruction to integrate the principle across existing IMA work.
- **Documentation completed on branch:** canonical charter plus cross-links and aligned requirements in the human-intelligence, global-identity/shared-learning, inner-song, creator-questions, backward-reflection, life-direction and continuous-evolution documents; README navigation updated.
- **PR:** [#138](https://github.com/imaosglobal/Ima-kernel/pull/138), merged by squash as commit `49a016501ba3e5a30811dfa2d072a5f75216e8e8`.
- **State:** DOCUMENTED_AND_MERGED / NOT_RUNTIME_VERIFIED / NOT_DEPLOYMENT_VERIFIED. This is not evidence of runtime integration.
- **Runtime code implementation (separate PR):** branch `feature/dynamic-identity-runtime` adds `core/dynamic_identity.py`, injects its policy through `core/human_intelligence.py::compose_prompt`, connects the canonical loop contract in `core/ima_loop.py`, removes the legacy “מי אני?” response shortcut from `ima_master_runtime.py`, and updates the no-provider fallback in `ima_mom.py`; adds `tests/test_dynamic_identity.py`.
- **Runtime PR:** [#139](https://github.com/imaosglobal/Ima-kernel/pull/139), merged as `94031873639e0afcf5c835eb9474a5ac38484b97`.
- **Regression test extension:** [#140](https://github.com/imaosglobal/Ima-kernel/pull/140), merged as `e2471bf8f2579950cd57c7f5f874cc6cc6d13bfa`.
- **Build-time test gate:** Docker image build for commit `874acea39f1547486cf419bfb5f2de68d17b8af4` ran all five dynamic-identity tests; Render build log records `Ran 5 tests` and `OK`.
- **Render deployment:** service `Ima` (`srv-d0r96hadbo4c73a4o910`) deployed commit `874acea39f1547486cf419bfb5f2de68d17b8af4`; deploy `dep-dbkgnt6c6qcc7394n130` reached status `live`.
- **State:** IMPLEMENTED_AND_MERGED_AND_DEPLOYED / FIVE_REGRESSION_TESTS_PASSED / LIVE_BEHAVIOR_NOT_VERIFIED. Existing canonical memory schema retained; no second identity or memory store created.
- **Remaining verification:** the dedicated GitHub Actions workflow is configured but no run/status has been surfaced through the available GitHub checks. A real chat request verifying the new identity prompt and fallback behavior remains outstanding.


## 2026-11-04 — Single-source, deployment deduplication and live-browser audit

**Audit scope:** canonical GitHub repository, Pages deployment workflow, current public website in Firecrawl Live Browser, repository tree, and continuity protocol.

### Verified public website
- Canonical public URL: `https://imaosglobal.github.io/Ima-kernel/` (HTTP 200).
- The root URL `https://imaosglobal.github.io/` is not the project site; do not use it as a second public target.
- Render `https://ima-915m.onrender.com/` is an API/backend service, not a second public website.
- At the time of the live browser capture, the deployed UI build and `version.json` both matched source SHA `835aafac68caf7ec23be7754c82072d18237259b`.
- A 390×844 mobile browser check exposed a visible responsive defect: navigation labels collapse into narrow vertical letter stacks. State: **VERIFIED_LIVE_DEFECT / FIX_PENDING**.
- Chat, Community and Shop sections currently show a Google sign-in gate when logged out. Google Identity iframe was present; a successful user login was not attempted.

### Deployment duplication finding and repair
- Before repair, `.github/workflows/deploy-ima-pages.yml` listened to `workflow_run` completions from multiple unrelated IMA workflows in addition to push/manual/repository-dispatch. This caused multiple production deployment runs for the same source SHA; several redundant runs were queued, cancelled, or overlapped.
- Removed the broad `workflow_run` trigger. Canonical deploy triggers are now only `push` to `main`, `workflow_dispatch`, and `repository_dispatch` type `ima-canonical-deploy`.
- `.github/workflows/ima-ui-pages.yml` is manual-only and deliberately has no deploy job. `.github/workflows/ima-gh-pages.yml` is retired and deliberately exits with an error to prevent a second publisher.
- The generated GitHub Pages `pages build and deployment` run attempted to package the repository root, failed at artifact upload, and skipped its deploy job. The canonical React artifact workflow remains the intended publisher.
- Workflow change is committed in `503e0ff233e66c1204dda9b0aca106042d824f08`. A successful canonical deployment of this commit has **not** yet been verified. The deployed UI remains the previously verified build until a successful run confirms otherwise.

### Repository duplication inventory
- Repository contains 50 branches, 77 workflow YAML files, and approximately 1,270 paths matching archive/backup/snapshot naming. These counts do not mean every item is active or a competing deployment.
- The repository tree contains multiple memory-like JSON/JSONL stores and adapters across legacy, archive, UI, founder, kernel and learning paths.
- Existing master-state evidence already identifies `conversation_layer.py` as retaining a separate legacy JSON conversation store beside the canonical universal-memory adapter. This remains an explicit reconciliation target.
- Do not mass-delete branches, backups, or memory files before tracing active readers/writers, comparing contents, preserving unique records, and verifying rollback. Historical artifacts must not be mistaken for active runtime authorities.

### Continuity and cross-chat status
- Consolidated the duplicated assistant-continuity protocol into `.ima/continuity/ASSISTANT_BIDIRECTIONAL_SYNC.md`; `.ima/chatgpt_bridge/PROTOCOL.md` now points to that canonical file.
- This is a durable project policy, not proof of automated synchronization. Cross-chat transport remains **NOT VERIFIED / PENDING AUTHENTICATED ENDPOINT**. ChatGPT UI histories cannot be merged by repository code.
- Firecrawl monitor for the canonical public URL and `version.json` is active on a six-hour schedule. It does not provide a permanent shared interactive browser session.

### Next required actions
1. Fix the mobile navigation collapse in the canonical React source and verify at 390px, tablet and desktop widths.
2. Obtain one successful canonical deployment for the current `main` SHA and verify the public version marker and `gh-pages` mirror.
3. Audit the 50 branches and 77 workflows; keep one production deploy path and classify every other workflow as QA, build-only, retired or genuinely required.
4. Trace all active memory readers/writers; migrate unique data into the canonical universal-memory runtime, then disable redundant writers only after backup and tests.
5. Implement and verify an authenticated, consent-aware continuity transport before claiming any cross-chat synchronization.


## 2026-11-04 20:15 — Authenticated live-browser Collaboration Bridge

- Request: activate a shared interactive browser inside IMA Chat after verified Google sign-in, with human takeover when available; keep Opera as a connector and Firecrawl/Browser Use-style alternatives behind one bridge.
- Implemented: public React Chat now contains a live-browser collaboration panel; backend exposes authenticated live-browser status/session/stop routes; client adapter is ima-ui/src/services/liveBrowserBridge.js.
- Provider: Firecrawl /v2/scrape plus /v2/scrape/{scrapeId}/interact, returning interactiveLiveViewUrl for human takeover. Provider capability was verified during this audit.
- Security boundary: first bridge opens only IMA's canonical public URL; session creation requires a valid IMA/Google bearer session; no unrestricted arbitrary-URL proxy.
- Opera: connector remains NOT_CONNECTED and its current exposed surface does not provide an embeddable takeover URL. Do not claim Opera integration is live.
- Deployment: Render service is currently LIVE on commit 58e4ff08b58c8bbf1bb26208359767294b5c2d15. GitHub Pages run 41886349195 is still pending and therefore public UI deployment is not yet verified.
- Blocker: Render does not yet have FIRECRAWL_API_KEY configured, so the live-browser session endpoint will remain 503 until the secret is added. The secret must never be committed to Git.
- Next: add FIRECRAWL_API_KEY to Render service srv-d0r96hadbo4c73a4o910, then verify authenticated session creation, iframe rendering, human takeover and clean stop; afterward verify GitHub Pages run and public browser smoke test.
