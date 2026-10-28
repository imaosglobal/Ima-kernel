# IMA Multi-Perspective Review Protocol

IMA is reviewed as one system from the viewpoint of the people, organizations, technical actors and environments affected by it. This is part of the single IMA Global Health Loop, not a second scheduler.

## Core rule
For every meaningful change, capability, integration, public surface or blocker:
**Who experiences this? What do they need? What can go wrong? What evidence exists? What is the smallest safe improvement? How does it affect the rest of IMA?**

## Canonical lenses
person/user; child; parent/caregiver; adult; older person; accessibility/disability; vulnerable/high-stress user; customer/buyer; CEO/executive; organization/operator; educator; researcher; developer/agent builder; creator; community member; public institution; security/privacy; legal/compliance; finance/sustainability; infrastructure/SRE; distribution/discovery; future/generational steward; environment/system-of-systems.

## Dimensions
usefulness/outcome; accessibility/inclusion; safety; privacy/consent/data minimization; human agency/intelligibility/contestability; truth/evidence/provenance; performance/reliability; security/abuse resistance; economics/sustainability; interoperability/provider independence; distribution/discoverability; governance/accountability; cultural/language impact; continuity/reversibility; effect on other IMA capabilities.

## Scale and time
Review at micro, product, macro and system-of-systems scales, and across now, near-term, one-year, multi-year and intergenerational horizons.

## Evidence
Statuses: SOURCE, IMPLEMENTED, TESTED, DEPLOYED, RUNTIME_VERIFIED, USER_VERIFIED, EXTERNAL_EVIDENCE, BLOCKED, UNKNOWN. Source code, documentation, generated state and intention are not runtime proof.

## Priority
P0 = immediate safety/privacy/security/agency/integrity/severe availability risk.
P1 = material user/product/business failure.
P2 = meaningful safe improvement.
P3 = exploratory/future preparation.

Safe authorized fixes may be executed immediately. Consequential external actions remain human-controlled.

## CEO/customer rule
Customer review covers outcome, trust, usability, accessibility, privacy, support, price/value, reliability, portability and exit.
CEO review covers mission, measurable outcomes, risk, economics, operational burden, governance, dependency/concentration, scalability and evidence.
A change is not an upgrade if it materially improves one stakeholder while degrading safety, truth, privacy, agency or another critical stakeholder without an explicit justified trade-off.

## Learning
Every review records: previous blocker -> new evidence/capability -> change -> test -> verification -> remaining blocker -> reusable lesson. Lessons return to the canonical loop rather than creating parallel automation.
