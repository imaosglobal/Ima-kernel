"""Evidence-bounded memory provenance.

Memory entries retain source, confidence and lifecycle state so corrections
and withdrawals can be represented without silently rewriting history.
"""

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class MemoryRecord:
    key: str
    value: str
    source: str
    confidence: float
    status: str = "ACTIVE"


def validate_memory(record: MemoryRecord) -> tuple[bool, str]:
    if not record.key or not record.source:
        return False, "missing_key_or_source"
    if not 0.0 <= record.confidence <= 1.0:
        return False, "confidence_out_of_range"
    if record.status not in {"ACTIVE", "CORRECTED", "WITHDRAWN"}:
        return False, "invalid_status"
    return True, "ok"


def correct_memory(record: MemoryRecord, new_value: str, source: str) -> dict:
    ok, reason = validate_memory(record)
    if not ok or not new_value or not source:
        return {"status": "REJECTED", "reason": reason if not ok else "missing_correction"}
    return {
        "previous": asdict(record),
        "replacement": asdict(MemoryRecord(record.key, new_value, source, record.confidence, "CORRECTED")),
    }


def withdraw_memory(record: MemoryRecord, reason: str) -> dict:
    ok, validation = validate_memory(record)
    if not ok:
        return {"status": "REJECTED", "reason": validation}
    if not reason.strip():
        return {"status": "REJECTED", "reason": "missing_withdrawal_reason"}
    return {"status": "WITHDRAWN", "record": asdict(MemoryRecord(
        record.key, record.value, record.source, record.confidence, "WITHDRAWN"
    )), "reason": reason.strip()}
