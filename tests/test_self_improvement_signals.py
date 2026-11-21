from learning.self_improvement_signals import derive_candidates


def test_high_error_rate_creates_candidate():
    items = derive_candidates({"error_rate": 0.10})
    assert items[0].area == "reliability"
    assert items[0].priority == "high"


def test_low_success_rate_creates_candidate():
    items = derive_candidates({"task_success_rate": 0.5})
    assert any(item.area == "task_success" for item in items)


def test_negative_feedback_is_evidence_not_execution():
    items = derive_candidates({}, [{"sentiment": "negative"}])
    assert items[0].area == "user_feedback"


def test_no_signal_means_no_candidate():
    assert derive_candidates({"error_rate": 0.01, "task_success_rate": 0.99}) == []
