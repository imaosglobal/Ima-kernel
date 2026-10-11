import json, tempfile, os
from pathlib import Path
import learning.direction_map as dm

def test_direction_map_roundtrip(tmp_path):
    dm.STORE = tmp_path / "direction_maps.json"
    user = "public:test-user"
    empty = dm.get(user)
    assert empty["schema_version"] == "1.0.0"
    assert empty["values"] == []

    updated = dm.add_entry(user, "values", {
        "content": "justice",
        "status": "FIRST_PERSON_REPORT",
        "provenance": "user_explicit",
    })
    assert len(updated["values"]) == 1
    entry_id = updated["values"][0]["id"]

    current = dm.get(user)
    assert current["values"][0]["content"] == "justice"

    removed, after = dm.delete_entry(user, "values", entry_id)
    assert removed is True
    assert after["values"] == []

def test_unknown_category_rejected(tmp_path):
    dm.STORE = tmp_path / "direction_maps.json"
    try:
        dm.add_entry("public:x", "unknown", {"content": "x"})
        assert False
    except ValueError:
        assert True
