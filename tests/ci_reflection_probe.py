"""CI probe: import the live reflection integration without side effects."""
from ima_runtime.reflection_runtime import reflect


def test_live_gate_records_unknown_without_independent_conclusion():
    record = reflect("probe", evidence=("probe-evidence",), context={"scope": "ci"})
    assert record["comparison"]["resolution_status"] == "UNRESOLVED"
    assert "TRUE_UNKNOWN" in record["comparison"]["gap_types"]
