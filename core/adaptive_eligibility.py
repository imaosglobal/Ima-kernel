"""Adaptive Eligibility Core — AE-001.

IMA adapts to conditions that determine whether a person, organization, feature,
route or offer is actually suitable and available. This layer does not make
legal, medical, financial, benefits or platform eligibility determinations.
Unknown conditions remain unknown until verified.
"""

VERSION = "AE-001-runtime-v1.0"

DOMAINS = (
    "accessibility", "language", "identity_and_consent", "capability",
    "privacy_and_safety", "revenue_and_payment", "benefits_and_reporting",
    "legal_and_tax", "deployment_and_device", "research_and_partnership",
)

HARD_BOUNDARIES = (
    "never_invent_eligibility",
    "never_treat_missing_evidence_as_eligible",
    "never_override_user_consent",
    "never_claim_legal_or_benefit_eligibility_without_authoritative_verification",
    "never_create_payment_or_legal_status_automatically",
    "adapt_the_route_before_rejecting_the_goal",
    "preserve_human_agency_and_reversibility",
)

def assess(requirements=None, evidence=None, capabilities=None, domain="general"):
    requirements = requirements if isinstance(requirements, dict) else {}
    evidence = evidence if isinstance(evidence, dict) else {}
    capabilities = capabilities if isinstance(capabilities, dict) else {}
    missing, blockers, matched = [], [], []
    for key, required in requirements.items():
        if required in (None, "", False):
            continue
        value = evidence.get(key)
        if value is None:
            missing.append(key)
        elif value == required or (isinstance(required, (list, tuple, set)) and value in required):
            matched.append(key)
        else:
            blockers.append(key)
    return {
        "contract": "AE-001",
        "runtime_version": VERSION,
        "domain": str(domain or "general"),
        "status": "eligible_if_verified" if not blockers and missing else ("adapt_route" if blockers else "eligible"),
        "matched": matched,
        "missing_verification": missing,
        "blockers": blockers,
        "available_capabilities": sorted(str(k) for k, v in capabilities.items() if v),
        "next_step": "verify_missing_requirements" if missing else ("adapt_route_to_blockers" if blockers else "proceed_with_user_consent"),
        "boundaries": list(HARD_BOUNDARIES),
    }

def build_context(message: str = "") -> str:
    return """
[IMA AE-001 ADAPTIVE-ELIGIBILITY BEHAVIOR]
Do not treat eligibility as a fixed binary question when conditions, access
routes or evidence can vary.

For every meaningful task:
1. identify actual eligibility or access requirements;
2. distinguish evidenced requirements from unknown requirements;
3. adapt language, accessibility, interface, capability, payment route, privacy
   level, device path and workflow to legitimate conditions;
4. when one route is unavailable, seek a lawful, consented alternative before
   treating the goal as impossible;
5. verify consequential eligibility with the authoritative source before making
   legal, benefits, tax, medical, financial or platform claims;
6. never infer eligibility from disability, nationality, income, age, identity
   or another sensitive attribute;
7. preserve agency: the person chooses consequential actions;
8. record route selection and evidence state so future interactions improve
   without pretending certainty.

The same contract applies to revenue: offer the route that fits actual payment
and rights conditions, but never convert a personal support route into a
business, donation, tax or benefits claim without verification.

Adaptation is a capability, not a promise that every external condition can
be satisfied. State what is blocked, unknown, and what alternative can be used.
""".strip()

def contract() -> dict:
    return {
        "contract": "AE-001",
        "runtime_version": VERSION,
        "status": "implemented_in_canonical_master_runtime",
        "domains": list(DOMAINS),
        "hard_boundaries": list(HARD_BOUNDARIES),
    }
