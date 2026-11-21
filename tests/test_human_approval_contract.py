from learning.human_approval_contract import evaluate_approval

def test_consequential_action_requires_confirmation():
    assert evaluate_approval(action_id="a", consequential=True, confirmed=False).status == "BLOCKED"
    assert evaluate_approval(action_id="a", consequential=True, confirmed=True).status == "ALLOWED"
    assert evaluate_approval(action_id="a", consequential=False, confirmed=False).status == "ALLOWED"
