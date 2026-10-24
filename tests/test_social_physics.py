from core.social_physics import SocialState, intervention_gate, observed_state, social_physics_contract, validate_status

def test_contract_is_research_only():
    c = social_physics_contract()
    assert c["epistemic_status"] == "research_framework"
    assert "higher_order" in c["network_models"]
    assert "privacy" in c["hard_constraints"]

def test_observation_does_not_replace_model_state():
    s = SocialState(state={"count": 10})
    r = observed_state(s, {"count": 9})
    assert r["model_state"]["state"]["count"] == 10
    assert r["observation"]["count"] == 9

def test_intervention_gate_preserves_agency():
    assert intervention_gate(expected_benefit=1, harm=0, agency_change=0)["accepted"]
    assert not intervention_gate(expected_benefit=1, harm=0.1, agency_change=0)["accepted"]
    assert not intervention_gate(expected_benefit=1, harm=0, agency_change=-0.1)["accepted"]

def test_status_rejects_unsupported_promotion():
    assert validate_status("SUPPORTED") == "SUPPORTED"
    try:
        validate_status("FACT")
    except ValueError:
        pass
    else:
        raise AssertionError("unsupported status was accepted")
