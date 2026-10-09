# IMA Human Intelligence — Implementation Roadmap
Updated: 2026-10-09
Status: implementation backlog and acceptance criteria; not a claim that all capabilities are implemented.

This roadmap operationalizes `docs/IMA_HUMAN_INTELLIGENCE_CHARTER.md`. It is the shared product direction for web, mobile/PWA, email, agents, integrations, memory, voice/3D and future interfaces. Do not create duplicate work items when an existing issue already tracks the same underlying blocker.

## P0 — Restore trustworthy verification
- Repair the malformed `tests/test_capability_factory.py` test class and run the affected test suite.
- Restore the health pipeline so skipped deployment/runtime/accessibility checks are reported explicitly rather than appearing green.
- Keep deployment status separate from verified runtime behavior.
Acceptance: tests pass in CI; health workflow reaches runtime checks; evidence links and exact commit SHA are recorded.

## P0 — Canonical human-centered memory
- Inspect and reconcile all existing memory stores/adapters before changing schemas.
- Replace no-op adapters only after confirming call sites, persistence contract, access boundaries and migration needs.
- Define a versioned event envelope: event ID, ISO-8601 UTC timestamp, source/interface, language, minimal participant identifiers, consent/authority basis, privacy class, original-content reference, translation/summary links, action/tool/result, verification, uncertainty, temporal scope (PAST/PRESENT/FUTURE), evidence references, retention and deletion state.
- Implement CAPTURE → CONSENT/CHECK → NORMALIZE → TIMESTAMP → CLASSIFY → STORE → INDEX → VERIFY → LEARN(if authorized) → AUDIT → RETAIN/DELETE.
- Never store credentials or secrets. Separate personal memory from global learning; default to no cross-user sharing. Provide export, correction and deletion paths.
Acceptance: tests cover consent denied, missing consent, user isolation, duplicate events, UTC normalization, retention/deletion, export, audit trail, and no learning from private content without authorization. Runtime test demonstrates actual persisted round-trip.

## P1 — Conversation understanding and response policy
- Add an explicit intent/need check: information, practical solution, listening/presence, creative collaboration, self-inquiry, relationship support, or other/uncertain.
- Distinguish observed facts, interpretations and hypotheses; communicate uncertainty in natural language.
- Ask clarifying questions only when the missing detail changes the answer materially.
- Support correction by the person and update the current interpretation without treating inferred emotions as facts.
- Evaluate empathy without flattery, truthfulness without cruelty, and support without creating dependency.
Acceptance: multilingual test set includes ambiguous requests, emotional disclosures, disagreement, corrections, culturally varied language and adversarial attempts to extract private memory; human review measures whether responses understood the need, were truthful and preserved agency.

## P1 — Interface-wide identity and accessibility
- Make the human-intelligence charter discoverable from all primary interfaces.
- Align Hebrew RTL and other localized interfaces, plain-language writing, keyboard/screen-reader behavior, mobile readability, and voice interaction.
- Treat avatars/voice as presentation layers, not proof of empathy or consciousness.
Acceptance: accessibility checks and language-specific UX checks run on the actual UI; no interface claims capabilities not present in runtime.

## P1 — Evidence-led learning and regression
- Record feedback, outcomes, source provenance and confidence with privacy-safe minimization.
- Promote learning only through authorized and validated paths.
- Maintain a regression suite for privacy boundaries, factual calibration, consent, deletion, response quality and memory retrieval.
Acceptance: each proposed behavioral improvement links to evidence, tests and a before/after result; failures update the shared backlog rather than silently changing behavior.

## P2 — Email and external actions
- Reconcile provider capabilities, mailbox authorization, history checkpoint and send quotas before processing.
- Deduplicate by provider message/thread ID and inspect Sent/thread context before reply.
- Draft for sensitive, ambiguous, legal, financial, medical, credential-related or commitment-bearing messages.
- Require authorization for consequential external actions; verify send outcomes before retrying.
Acceptance: no claim of completed history or sent mail without provider evidence; checkpoint advances only after verified batch completion.

## P2 — Trend-to-Brand and commerce
- Keep discovery, evidence, opportunity proposal, pilot, partnership, live product and actual revenue as separate states.
- Require multiple independent sources, source timestamps, geographic/language scope, bias and uncertainty notes.
- Validate demand and unit economics before manufacturing; verify suppliers, local regulations, platform availability and creator rights.
- Require human approval for outreach, spending, contracts, publication, orders and payment.
Acceptance: sample opportunity cannot be labeled validated without sufficient independent evidence and purchase-intent signal; no sales/ROI claims without real records.

## Shared status vocabulary
PLANNED / ATTEMPTED / EXECUTED / VERIFIED / FAILED / GAPS_RECORDED

Every cycle records ISO-8601 UTC time, workstream, owner, dependencies, status, source, evidence, assumptions, limitations, last checked and next action. Reuse findings from the same cycle and avoid duplicate daily jobs.

## Definition of done for the identity shift
The identity shift is not complete when this document is written. It is complete only when:
1. The charter is reflected in prompts/policies and actual UI across interfaces.
2. Canonical memory and consent boundaries pass runtime tests.
3. Conversation quality is evaluated against the charter with regression evidence.
4. Health checks verify deployed behavior rather than only repository or dashboard state.
5. Every claimed capability has reproducible evidence, and remaining gaps are visible.
