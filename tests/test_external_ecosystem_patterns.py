from learning.external_ecosystem_patterns import normalize_lessons

def test_requires_conflict_and_adaptation_fields():
    result = normalize_lessons([{
        "source":"example",
        "domain":"accessibility",
        "lesson":"stable references",
        "overlap":"LIVE-001",
        "adaptation":"observation-only mapping",
    }])
    assert result[0]["status"] == "REVIEW_REQUIRED"
    assert normalize_lessons([{"source":"bad"}]) == []
