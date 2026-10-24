from pathlib import Path

from learning.questions.question_memory import (
    question_memory_contract,
    record_question,
    validate_timestamp,
)


def test_question_memory_contract():
    contract = question_memory_contract()
    assert contract["captures_user_questions"] is True
    assert contract["requires_authoritative_timestamp"] is True
    assert contract["zero_point_protocol"].endswith("IMA_ZERO_POINT_DISCOVERY_PROTOCOL.json")


def test_authoritative_timestamp_required():
    assert validate_timestamp("2026-10-24")
    assert validate_timestamp("2026-10-24T12:34:56+03:00")
    assert not validate_timestamp("not-a-date")
    assert not validate_timestamp("2026-10-24 12:34:56")


def test_record_question_keeps_authorship_distinct():
    item = record_question(
        "מה יש כשהכל יש?",
        "current_chat",
        "2026-10-24",
        question_id="test_001",
    )
    assert item["attribution"] == "ORI_AUTHORED"
    assert item["question"] == "מה יש כשהכל יש?"
