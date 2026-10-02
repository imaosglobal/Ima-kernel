"""Dependency-free runtime comparison primitives for IMA's reflection protocol."""
from dataclasses import dataclass, asdict

GAP_TYPES = ("EVIDENCE_GAP","INTERPRETATION_GAP","ASSUMPTION_GAP","OBJECTIVE_GAP","SCOPE_GAP","CAPABILITY_GAP","UNCERTAINTY_GAP","VALUE_GAP","TRUE_UNKNOWN")

@dataclass(frozen=True)
class Conclusion:
    claim: str
    evidence: tuple
    assumptions: tuple = ()
    uncertainty: str = ""
    proposed_next_step: str = ""

@dataclass(frozen=True)
class Comparison:
    ima: Conclusion
    independent: Conclusion
    agreement: bool
    differences: tuple
    gap_types: tuple
    resolution_status: str

def compare(ima: Conclusion, independent: Conclusion) -> Comparison:
    differences=[]; gaps=[]
    if ima.claim != independent.claim:
        differences.append("claim")
        gaps.append("EVIDENCE_GAP" if ima.evidence != independent.evidence else "INTERPRETATION_GAP")
    if ima.assumptions != independent.assumptions:
        differences.append("assumptions"); gaps.append("ASSUMPTION_GAP")
    if ima.uncertainty != independent.uncertainty:
        differences.append("uncertainty"); gaps.append("UNCERTAINTY_GAP")
    if ima.proposed_next_step != independent.proposed_next_step:
        differences.append("next_step")
    return Comparison(ima, independent, not differences, tuple(dict.fromkeys(differences)), tuple(dict.fromkeys(gaps)), "AGREEMENT" if not differences else "UNRESOLVED")

def to_record(comparison):
    return asdict(comparison)

def self_test():
    a=Conclusion("same",("fact",),(),"low","verify")
    assert compare(a,a).agreement
    b=Conclusion("different",("other",),(),"low","verify")
    r=compare(a,b)
    assert not r.agreement and "EVIDENCE_GAP" in r.gap_types
    return {"ok":True,"agreement":to_record(compare(a,a)),"gap":to_record(r)}

if __name__ == "__main__":
    print(self_test())
