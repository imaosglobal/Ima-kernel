# IMA — Knowledge → Capability Protocol

## Purpose

IMA does not stop at learning that something exists. For every meaningful
knowledge item, the system creates an **Applied Skill** record describing how
that knowledge could become an actual capability.

The pipeline is:

**LEARN → UNDERSTAND → MODEL → SPECIFY → BUILD → TEST → VERIFY → USE → OBSERVE → UPGRADE**

This applies across domains: software, science, space, XR, robotics, smart
homes, education, accessibility, creative work, commerce, transport and
future technologies.

## Example: space travel

Learning "a spacecraft uses orbital mechanics" is knowledge.

An Applied Skill must additionally identify:

- the goal: navigate from one orbital state to another;
- required models: orbital state, propulsion, mass, constraints;
- interfaces: simulation, telemetry, navigation/control interfaces;
- implementation: simulator or bounded software adapter;
- tests: known orbital-transfer cases and failure cases;
- verification: compare observed results with expected results;
- limits: simulation is not a flight-qualified spacecraft system;
- upgrade path: improve the model, retest, then promote only with evidence.

The same pattern applies to every other field.

## Technology discovery

IMA continuously discovers technologies relevant to a learned problem and
records them as candidate adapters. A technology is not considered operational
because documentation says it exists. It moves through:

DISCOVERED → SPECIFIED → IMPLEMENTED → TESTED → VERIFIED → LIVE

Only the final state permits a public LIVE capability claim.

NASA's Technology Readiness Level model is a useful external precedent for
separating conceptual knowledge from tested technology maturity. NASA defines
TRL 1–9 from basic research through systems test/operations and emphasizes
determining maturity from what was actually demonstrated and under what
conditions. citeturn0search0turn0search7

## Verification before promotion

Every promoted skill should have:

1. a reproducible input;
2. an expected result;
3. an observed result;
4. a test environment;
5. provenance;
6. known limitations;
7. a rollback/disable path.

## Continuous improvement

When a verified capability is observed to fail or underperform, IMA creates a
new improvement cycle rather than silently replacing the capability:

OBSERVE → DIAGNOSE → SPECIFY → PATCH → REGRESSION TEST → VERIFY → PROMOTE

## Human control

Learning itself does not authorize external action. Purchases, messages,
advertising spend, device control, medical/financial decisions, vehicle
control and other consequential operations require explicit authorization and
the relevant provider/device permissions.

## Current implementation boundary

The repository now contains:

- an Applied Skill compiler;
- a persistent skill record format;
- a skill registry contract;
- application and verification stages;
- safety and provenance requirements.

This does **not** mean every domain is already operational. Individual
capabilities become LIVE only after implementation and executable verification.
