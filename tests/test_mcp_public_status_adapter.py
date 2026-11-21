from runtime.mcp_public_status_adapter import (
    public_distribution,
    public_learning_policy,
    public_status,
)


def test_public_status_contains_no_private_data():
    result = public_status()
    assert result["status"] == "verified_public_runtime"
    assert result["privacy"] == "public-runtime-only"
    assert "memory" not in result


def test_learning_policy_is_evidence_bounded():
    assert "no fabricated learning" in public_learning_policy()["policy"]


def test_distribution_requires_opt_in_and_approval():
    result = public_distribution()
    assert result["canonical"] == "imaosglobal/Ima-kernel"
    assert result["distribution"] == "opt-in"
    assert result["human_approval_required_for_connection"] is True
