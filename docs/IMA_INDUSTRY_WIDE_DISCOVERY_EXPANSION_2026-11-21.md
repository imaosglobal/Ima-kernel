# IMA Industry-Wide Discovery Expansion — 2026-11-21

## Implemented now

- Expanded the daily capability taxonomy to more than 80 industry domains.
- Added dedicated coverage for 3D/game engines, finance/banking/payments, marketing/sales/CRM, home services including plumbing/electrical/HVAC, design/web design, construction/real estate, robotics/hardware, science/space, healthcare, education, accessibility, public services, media, travel, food, sports and other sectors.
- Daily discovery now searches both GitHub repository metadata and broad web/news signals through GDELT.
- Added detection of previously unlisted industry terms from discovery topics as REVIEW_REQUIRED candidates.
- Added a canonical cross-industry pattern adapter that converts reusable lessons into IMA workflow candidates.
- Added regression tests for taxonomy and adaptation contracts.
- Added the discovery and adaptation modules to the canonical module registry.
- Added capability-registry and unified-repository mappings.
- The existing daily schedule remains the permanent execution mechanism.

## Safety boundary

Discovery is not capability proof. External code, secrets, credentials, branding and proprietary implementation are never copied. Consequential actions remain explicitly approved. IMA keeps one canonical brain/runtime, memory authority, feedback authority and LIVE-001 browser/device surface.

## Evidence

Relevant commits:
- 63b5e42915f4fd3f2121d0296096d93d2ad4a358 — industry taxonomy/patterns
- 6cc1e9e38778aa3f7cc0513d25e5c388dad412e4 — taxonomy tests
- b8ada9b2beee3af33dad953c099b83bd7200cd46 — permanent discovery contract
- 5ac9e04016d85f68867a55794728ba3eaa54d2c0 — expanded industry scanner
- 59f3084786aa1e34d7354510afacf1571bfdfcc5 — completed GitHub + GDELT scan
- 3356a31cee84bb3ddf381a32442125913c1a8e68 — canonical pattern adapter
- d97ee95906c681f5c183dbff160b492ee166d85c — adapter tests
- 31f32febe9eaebc149dc405bb1a0e9b9108ac174 — new-domain detection
- a3d92894c7a2dbbb76361f7d96b48b7d172b26f7 — permanent daily workflow integration

CI/runtime verification of these newest commits is still required; no pass is claimed until observed.
