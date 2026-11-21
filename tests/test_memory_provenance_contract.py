from learning.memory_provenance_contract import MemoryRecord, validate_memory, correct_memory, withdraw_memory

def test_memory_lifecycle():
    record = MemoryRecord("k", "old", "user", 0.9)
    assert validate_memory(record)[0]
    assert correct_memory(record, "new", "user")["replacement"]["status"] == "CORRECTED"
    assert withdraw_memory(record, "user requested removal")["status"] == "WITHDRAWN"
