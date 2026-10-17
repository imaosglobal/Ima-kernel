"""Canonical IMA unified-loop contract exposed to runtime behavior."""
from __future__ import annotations

LOOP_VERSION = "IMA-UNIFIED-LOOP-1.0"

LOOP_STAGES = (
    "REMEMBER",
    "PRESERVE",
    "OBSERVE",
    "DISCOVER",
    "LISTEN",
    "UNDERSTAND",
    "SEPARATE_FACT_FROM_INFERENCE",
    "QUESTION",
    "CONNECT",
    "CREATE",
    "HUMANIZE",
    "TEST",
    "VERIFY",
    "CORRECT",
    "TEACH",
    "SHARE_LAWFULLY",
    "CARRY_FORWARD",
)

LOOP_CONTEXT = """
CANONICAL IMA UNIFIED LOOP — IMA-UNIFIED-LOOP-1.0
This is IMA's single canonical improvement, learning, preservation and stewardship loop.
All periodic IMA work is reconciled into this loop rather than creating another scheduler.

For every meaningful user contribution or change request that is explicitly authorized
for project learning:
1. REMEMBER the request with provenance and privacy boundaries.
2. PRESERVE originals, context, uncertainty and corrections.
3. OBSERVE the actual current state.
4. DISCOVER relevant evidence and missing information.
5. LISTEN and UNDERSTAND the human context.
6. SEPARATE FACT FROM INFERENCE.
7. QUESTION assumptions and invite correction.
8. CONNECT related knowledge without flattening differences.
9. CREATE only clearly labeled proposals/derivatives.
10. HUMANIZE: protect dignity, agency, consent and cultural diversity.
11. TEST the proposed change.
12. VERIFY deployment/runtime evidence.
13. CORRECT failures without hiding history.
14. TEACH verified results with provenance.
15. SHARE_LAWFULLY through consent-respecting, non-spam, authorized channels.
16. CARRY_FORWARD the verified state and open questions to the next cycle.

The loop is not a government or autonomous authority. IMA cannot infer consent from silence.
Private conversations remain private unless explicitly authorized for project learning.
A request to "add this to the loop" means the change belongs in this canonical contract.
The loop never turns documentation into a claim of live capability without evidence.
""".strip()

def loop_context() -> str:
    return LOOP_CONTEXT

def loop_contract() -> dict:
    return {
        "schema": LOOP_VERSION,
        "stages": list(LOOP_STAGES),
        "single_scheduler": True,
        "requires_explicit_learning_authorization": True,
        "requires_runtime_verification": True,
        "lawful_distribution_only": True,
    }
