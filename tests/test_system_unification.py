import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "IMA_SYSTEM_UNIFIED_CONTRACT.json"
ZERO = ROOT / "research/IMA_ZERO_POINT_DISCOVERY_PROTOCOL.json"
ENERGY = ROOT / "research/IMA_ENERGY_INTERNAL_DISCOVERY.json"
AUTH = ROOT / "LEARNING_AUTHORITY_MAP.json"
APPROVED = ROOT / "APPROVED_LEARNING_INTEGRATION.json"

class SystemUnificationContractTest(unittest.TestCase):
    def test_single_canonical_system(self):
        c=json.loads(CONTRACT.read_text(encoding="utf-8"))
        z=json.loads(ZERO.read_text(encoding="utf-8"))
        e=json.loads(ENERGY.read_text(encoding="utf-8"))
        a=json.loads(AUTH.read_text(encoding="utf-8"))
        p=json.loads(APPROVED.read_text(encoding="utf-8"))
        self.assertEqual(c["status"],"CANONICAL")
        self.assertEqual(c["canonical_authorities"]["brain_orchestrator"],"learning/meta_orchestrator.py")
        self.assertEqual(c["canonical_authorities"]["runtime"],"kernel/runtime/CANONICAL/python_bridge.py")
        self.assertEqual(a["memory_authority"],"learning/learning_memory.py")
        self.assertEqual(a["feedback_authority"],"learning/feedback_engine.py")
        self.assertEqual(z["status"],"CANONICAL")
        self.assertEqual(e["canonical_zero_point"],"research/IMA_ZERO_POINT_DISCOVERY_PROTOCOL.json")
        self.assertEqual(e["loop"][0],"ZERO")
        self.assertEqual(e["loop"][-1],"ZERO")
        self.assertIn("learning/learning_memory.py",p["learning_core"])
        self.assertIn("learning/feedback_engine.py",p["learning_core"])
        self.assertTrue(any("One canonical brain/orchestrator" in x for x in c["authority_rules"]))
        self.assertTrue(any("One canonical ZERO" in x for x in c["authority_rules"]))

if __name__ == "__main__":
    unittest.main()
