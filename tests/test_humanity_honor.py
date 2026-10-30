import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "humanity_honor", ROOT / "core/humanity_honor.py"
)
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MOD)


def test_humanity_honor_preserves_worth_and_agency():
    result = MOD.assess("קשה לי")
    assert result.ego_release_recommended
    assert result.self_humor_allowed
    assert result.compasion_priority if False else result.compassion_priority
    assert result.agency_preserved
    assert result.boundaries_preserved
    assert result.truth_preserved


def test_humanity_honor_contract_has_unconditional_regard_and_giving():
    contract = MOD.contract()
    assert "UNCONDITIONAL_REGARD_WITHOUT_OWNERSHIP_OR_DEPENDENCY" in contract["principles"]
    assert "GIVE_VALUE_WITHOUT_UNNECESSARY_ENERGY_EXTRACTION" in contract["principles"]
    assert "NO_FORCED_POSITIVITY" in contract["guardrails"]
