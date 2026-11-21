from learning.permanent_quality_guard import (
    evaluate_quality_signals,
    quality_summary,
)


def test_all_required_areas_pass():
    signals = {
        "buttons": True,
        "authentication": True,
        "pwa": True,
        "accessibility": True,
        "performance": True,
        "security": True,
        "routing": True,
    }

    findings = evaluate_quality_signals(signals)

    assert all(item.status == "PASSED" for item in findings)
    assert quality_summary(findings)["healthy"] is True


def test_failed_signal_is_reported_without_mutation():
    signals = {"buttons": False}

    findings = evaluate_quality_signals(signals, required_areas=["buttons"])

    assert findings[0].status == "FAILED"
    assert findings[0].severity == "error"
    assert signals == {"buttons": False}


def test_missing_signal_is_not_invented_as_failure():
    findings = evaluate_quality_signals({}, required_areas=["authentication"])

    assert findings[0].status == "NOT_OBSERVED"
    assert findings[0].severity == "warning"
    assert quality_summary(findings)["healthy"] is False


def test_summary_counts():
    findings = evaluate_quality_signals(
        {"buttons": True, "authentication": False},
        required_areas=["buttons", "authentication", "routing"],
    )

    assert quality_summary(findings) == {
        "passed": 1,
        "failed": 1,
        "not_observed": 1,
        "healthy": False,
    }
