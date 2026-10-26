from .ima_self_worth import assess_self_worth


def test_self_worth_detects_shame_without_diagnosing():
    result = assess_self_worth("אני שונא את עצמי ולכן כולם נגדי")
    assert result["self_directed_harm_language"]
    assert result["diagnosis"] == "NOT_DIAGNOSED"
    assert result["agency_preserved"]


def test_group_hatred_is_separated_from_person_worth():
    result = assess_self_worth("הם כולם מפלצות")
    assert result["group_dehumanization"]
    assert "PERSON_IS_NOT_A_GROUP" in result["principles"]


def test_neutral_text_is_low_risk():
    result = assess_self_worth("אני רוצה ללמוד איך להתנהל טוב יותר עם אנשים")
    assert result["risk_level"] == "LOW"
