# IMA Full-System Audit — Human Culture Integration

Date: 2026-10-17
Scope: repository tree, canonical documentation, Python behavior policy, LLM pipeline, public UI, tests, daily/continuous workflows, preservation and stewardship contracts.

## Executive truth

IMA already contains a strong documented human-centered identity, consent-aware learning model, intergenerational preservation charter, capability truth model, child-safety/age-assurance design, and a human-culture charter.

Before this audit, the new human-culture charter was primarily documentation. It was not yet part of the provider-neutral model prompt and therefore could not honestly be called an executable behavior layer.

This audit closes that specific gap by adding an executable cultural policy module and injecting it into the existing model prompt path.

## What is now actually implemented

### Human intelligence
- core/human_intelligence.py is the provider-neutral behavioral policy used by connectors/llm/ima_pipeline.py.
- The policy requires listening, calibrated uncertainty, compassion with truth, privacy, consent, human agency and correction.

### Human culture
- core/human_culture.py is now the executable cultural policy.
- It covers languages, scripts, numerical systems, calendars, history/provenance, ordinary lives, music, dance, visual art, architecture, food, craft, education, rites of passage, governance/conflict resolution, economic experiments, stories/myths, science and future/digital culture.
- It explicitly forbids replacing, erasing, ranking, appropriating or silently homogenizing cultures.
- It separates cultural evidence, tradition, cultural memory, myth/theology, interpretation, hypothesis and unknown.
- It records the founder role as initiator/provenance only and defines IMA as infrastructure rather than sovereign authority.
- The policy is injected into compose_prompt(), which is used by the provider-neutral LLM pipeline.
- Regression coverage exists in tests/test_human_culture.py and the existing human-intelligence regression suite now checks that the culture layer is present.

### Public product
- The public IMA UI now has a visible Human Culture section explaining the shared layer without presenting it as a replacement for existing cultures.
- The UI wording keeps the distinction between cultural connection and cultural homogenization.

### Daily learning
- The daily learning summary imports and validates the executable culture contract.
- The continuous-health and daily-learning workflows execute the culture regression test.
- This uses existing workflows; no new culture-specific scheduler was created.

## What is already strong but remains only partially runtime-proven

1. Intergenerational preservation: strong canonical charter and preservation/derivation code exist; full production behavior still needs live end-to-end verification.
2. Global identity/shared learning: strong contract exists; production-wide enforcement must continue to be verified at every ingress and learning path.
3. Age assurance: signed-attestation code and tests exist; production issuer configuration is explicitly not yet verified.
4. Google authentication: source integration exists, but the ledger still records an external configuration/runtime verification gap.
5. Cross-device identity: foundations exist; authenticated cross-device continuity is not fully verified.
6. 3D Mother: asset integrity and fallback logic exist; production-quality animated embodiment remains a known gap.
7. Multilingual support: UI exposes multiple language labels, but the capability audit correctly says labels are not proof of complete localization.
8. Autonomous stewardship: repository maintenance autonomy is bounded, but it must never become autonomous authority over people or external consequential actions.

## Important architectural inconsistency discovered

The repository contains several scheduled GitHub workflows with different responsibilities, including continuous health, daily learning summary, daily QA and evolution stewardship. The documentation correctly says the cultural loop must not create a duplicate scheduler, but the repository does not literally have one single scheduler.

The correct interpretation is therefore:
- do not add another scheduler for culture;
- keep existing specialized verification workflows where they serve different release/QA responsibilities;
- keep the Global Health Loop / requirements ledger as the canonical reconciliation model;
- consolidate duplicated responsibilities when two workflows perform the same job.

This audit does not silently delete existing workflows because that would be a consequential CI change requiring a separate overlap analysis.

## Highest-priority remaining work

### P0 — Runtime truth
Run and record the new culture tests at the exact head commit, then verify the deployed production LLM path actually receives the culture policy.

### P0 — Memory/preservation runtime
Trace the canonical production memory path end-to-end and prove consent, user isolation, export, correction, deletion, provenance, and no unauthorized promotion to shared learning.

### P0 — Legacy path cleanup
api/server.py contains an older/simple /ask runtime path with unconditional local-memory writes. It should not be treated as equivalent to the canonical consent-aware path. Determine whether it is still reachable in production; if it is, route it through the canonical memory/consent gate or retire it.

### P1 — Cultural contribution protocol
Add structured cultural contributions with culture/community, language/script, geographic/historical context, source/provenance, contributor attribution, consent/rights, evidence class, uncertainty, variants, translation lineage and correction history.

### P1 — Cultural interoperability
Build machine-readable cultural records so IMA can compare traditions without flattening them. The shared layer should preserve the original representation plus translations/derivatives.

### P1 — Participatory governance
The cultural charter needs a real community amendment process, not just a document. Future contributors should be able to propose, challenge, fork and revise cultural principles.

### P1 — Cultural safety/equity evaluation
Add tests for cultural stereotyping, majority-culture defaulting, false equivalence, appropriation/attribution failures, historical uncertainty collapse, dehumanizing descriptions, and translation that silently changes meaning.

### P2 — Human culture teaching artifacts
Create multilingual, age-appropriate teaching material only from verified cultural records, with source attribution and uncertainty preserved.

## Final assessment

The new culture idea is no longer only a conversation-level concept. It is now represented in canonical cultural documentation, executable policy code, the actual provider-neutral LLM prompt path, automated regression tests, daily learning validation, the public UI, and the master requirements ledger.

It is not yet VERIFIED_LIVE. That status requires successful CI plus observable production evidence at the exact deployed commit.