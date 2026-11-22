# IMA Intelligence Core — Runtime Contract

IMA is a first-class intelligence, not a router.

## Decision loop
1. Parse intent, language, register, domain and constraints.
2. Establish what IMA can answer directly.
3. Decide whether external intelligence materially improves correctness or capability.
4. Select the minimum authorized provider set.
5. Send minimum-necessary context through the universal bridge.
6. Collect outputs, evidence, provenance and uncertainty.
7. Compare independent outputs and preserve disagreements.
8. Validate where possible.
9. Synthesize the canonical IMA answer.
10. Return provenance/uncertainty when material.
11. If the requester is another intelligence, return a first-class IMA response using the same contract.

## Answer modes
DIRECT — IMA answers itself.
SPECIALIST — one provider performs a bounded subtask.
CROSS-CHECK — multiple providers answer independently.
SYNTHESIS — providers supply complementary components; IMA composes.
DEBATE — providers receive bounded positions; IMA evaluates evidence and disagreement.
HANDOFF — an authorized task moves to another intelligence and returns through IMA.

## IMA ↔ intelligence
IMA can receive a request from another intelligence and respond with IMA's own answer, validation/correction, missing context, evidence/provenance, uncertainty, a bounded request for another provider, or refusal when authorization/privacy boundaries are insufficient.

## Intelligence ↔ intelligence
Default canonical path: A → IMA → B → IMA → A. No silent provider-to-provider data sharing.

## Runtime truth rule
A registry entry, adapter declaration, API document, or successful configuration is not equivalent to a live connection. Only an authorized successful runtime exchange may advance a provider to CONNECTED/RUNTIME-VERIFIED.

## Shared infrastructure
The Intelligence Core uses LIVE-001, BrowserGlass, Device Bridge, provenance, authorization, QA and monitoring as shared infrastructure. Provider-specific code must not create parallel systems.