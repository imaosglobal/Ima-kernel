import json
import unittest
from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/".ima/evolution/self_timeline.py"
spec=importlib.util.spec_from_file_location("self_timeline",TARGET)
module=importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

class SelfTimelineTests(unittest.TestCase):
    def test_history_seed_is_present(self):
        data=json.loads((ROOT/".ima/evolution/HISTORY_SEED.json").read_text(encoding="utf-8"))
        self.assertTrue(data["entries"])
        self.assertTrue(any(e["event"]=="continuous_stewardship" for e in data["entries"]))

    def test_archive_inventory_is_nonempty(self):
        inv=module.archive_inventory()
        self.assertGreater(inv["files"],0)
        self.assertTrue(inv["families"])

    def test_timeline_build_has_open_gap_state(self):
        t=module.build()
        self.assertEqual(t["schema"],"IMA-SELF-TIMELINE-1.0")
        self.assertGreaterEqual(t["current_gaps"]["total"],1)
        self.assertGreater(t["archive_inventory"]["files"],0)

if __name__=="__main__":
    unittest.main()
