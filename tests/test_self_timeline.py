import json
from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/".ima/evolution/self_timeline.py"
spec=importlib.util.spec_from_file_location("self_timeline",TARGET)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def test_history_seed_is_present():
    data=json.loads((ROOT/".ima/evolution/HISTORY_SEED.json").read_text(encoding="utf-8"))
    assert data["entries"]
    assert any(e["event"]=="continuous_stewardship" for e in data["entries"])

def test_archive_inventory_is_nonempty():
    inv=m.archive_inventory()
    assert inv["files"]>0
    assert inv["families"]

def test_timeline_build_has_open_gap_state():
    t=m.build()
    assert t["schema"]=="IMA-SELF-TIMELINE-1.0"
    assert t["current_gaps"]["total"]>=1
    assert t["archive_inventory"]["files"]>0
