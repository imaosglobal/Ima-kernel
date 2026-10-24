from pathlib import Path

PROFILE = Path("docs/IMA_ORI_CAPABILITY_GROWTH_PROFILE.md")

def test_profile_exists():
    assert PROFILE.exists()

def test_profile_preserves_zero_point_and_agency():
    text = PROFILE.read_text(encoding="utf-8")
    assert "Return to ZERO" in text
    assert "Improve capability, not worth." in text
    assert "No psychological diagnosis" in text

def test_profile_distinguishes_status():
    text = PROFILE.read_text(encoding="utf-8")
    for token in ["conceived", "specified", "implemented", "tested", "deployed", "observed in production"]:
        assert token in text
