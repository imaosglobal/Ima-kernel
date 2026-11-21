from learning.agent_security_regression import check_action_gate, check_secret_boundary, check_memory_poisoning

def test_security_boundaries():
    assert not check_action_gate(consequential=True, confirmed=False).passed
    assert check_action_gate(consequential=True, confirmed=True).passed
    assert not check_secret_boundary(text="api_key=secret").passed
    assert check_memory_poisoning(source="user", value="fact").passed
