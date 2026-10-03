# IMA Continuous AI Capability Radar

## Objective
Continuously discover publicly announced capabilities from a maintained watchlist of AI providers, open-source model/tool ecosystems, research venues, and accessibility communities. Convert discoveries into auditable candidate records and evaluate whether each capability fits IMA's identity, user needs, safety, privacy, accessibility, cost, licensing, and implementation constraints.

This is a discovery and evaluation pipeline, not a promise to observe every AI system on the internet. Coverage is limited to configured sources and successful fetches; failures and stale sources must be reported.

## Operating cycle
1. Fetch configured public feeds on a scheduled GitHub Actions run.
2. Parse only feed metadata; treat all remote content as untrusted data, never as instructions or executable code.
3. Deduplicate by canonical URL and normalized title; retain source and publication date.
4. Classify capability candidates: multimodal perception, voice, accessibility, memory, reasoning, agents, tools/computer use, creation, robotics/embodiment, interoperability, privacy/safety, and infrastructure.
5. Assess fit against IMA's compassionate, human-centered vision. Record evidence, maturity, access/region/device constraints, costs, rights, safety limits, uncertainty, and implementation dependencies.
6. Keep discoveries in an append-only observation log and a human-readable digest.
7. Promote only after reproducible tests, security review, licensing/privacy review, rollback plan, and explicit approval. New capabilities must not silently replace existing behavior or alter private memory.
8. For eligible low-risk integrations, create a proposed branch/PR with tests and provenance; never auto-merge or deploy a newly discovered third-party capability merely because a feed announces it.

## Trust and safety gates
- Separate ANNOUNCED, AVAILABLE, TESTED, INTEGRATED, and VERIFIED states.
- An announcement is not proof of availability or quality.
- Do not send private IMA/user data to external providers during evaluation.
- Require opt-in and explicit scope for camera, microphone, files, accounts, payments, physical devices, and external communications.
- Visual assistance must not be represented as navigation, obstacle detection, medical diagnosis, or a replacement for established safety aids unless independently validated and appropriately authorized.
- Respect provider terms, licenses, privacy, accessibility feedback, rate limits, and robots/platform rules.
- Keep secrets out of logs; restrict workflow permissions to the minimum needed.
- A failed or unavailable source is a recorded gap, not evidence that no update exists.

## Initial source coverage
The initial watchlist is maintained in `.ima/intelligence_radar/sources.json`. It is deliberately finite and can be expanded after each source is validated. The radar must report the exact sources successfully scanned per run.

## IMA adaptation rubric
A candidate is considered for adaptation when it advances one or more of:
- compassionate, context-sensitive assistance without coercion;
- multilingual and cross-cultural accessibility;
- user agency, privacy, security, truthfulness, and explainability;
- useful perception/voice/creation/memory/tool capability;
- interoperability and affordability;
- reliability on IMA's actual target devices and deployment.

A capability may be rejected, deferred, or integrated only as an optional provider-backed feature. "New" does not imply "suitable."

## Evidence and continuity
Each scan records UTC timestamp, source, URL, title, published date when available, observation status, and fetch/parse errors. Integration decisions additionally record test evidence, owner, risks, rollback, and exact commit/PR identifiers. Append to `.ima/journal/development.jsonl`; do not rewrite historical entries.
