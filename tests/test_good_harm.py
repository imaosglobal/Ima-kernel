from core.ima_good_harm import good_harm_contract

def test_good_harm_contract_has_core_guards():
    c = good_harm_contract()
    assert c["improve_human_worth"] is False
    assert c["requires_evidence_and_uncertainty"] is True
    assert c["agency_must_not_decrease_by_default"] is True
    assert c["minimum_effective_intervention"] is True
    assert c["return_to_zero_when_uncertain"] is True
