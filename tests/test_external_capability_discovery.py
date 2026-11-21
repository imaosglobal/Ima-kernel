from learning.external_capability_discovery import normalize_candidates

def test_normalizes_only_complete_candidates():
    result = normalize_candidates([
        {"source":"github","name":"x","evidence_url":"https://example.test/x","capability":"browser"},
        {"source":"github","name":"bad","evidence_url":"","capability":"browser"},
    ])
    assert len(result) == 1
    assert result[0]["conflict_status"] == "REVIEW_REQUIRED"
