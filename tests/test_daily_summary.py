import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / ".ima" / "web_intelligence" / "daily_summary.py"

spec = importlib.util.spec_from_file_location("daily_summary", TARGET)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_daily_summary_uses_israel_timezone():
    assert str(module.TZ) == "Asia/Jerusalem"


def test_concrete_lessons_are_derived_from_evidence():
    events = [{
        "summary": "Fixed a real defect",
        "status": "VERIFIED",
        "details": {
            "observations": ["Observed a failing contract"],
            "next": ["Run smoke test"],
        },
    }]
    lessons = module.concrete_lessons(events)
    assert "Fixed a real defect [VERIFIED]" in lessons
    assert "Observed a failing contract" in lessons
    assert "Run smoke test" in lessons


def test_daily_question_is_present_in_source():
    source = TARGET.read_text(encoding="utf-8")
    assert "מה עוד ניתן לשפר באמא היום?" in source
    assert "improvements_executed" in source
