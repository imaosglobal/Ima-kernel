import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHARTER = ROOT / "research" / "IMA_ENERGY_INTERNAL_DISCOVERY.json"

class EnergyInternalDiscoveryContractTest(unittest.TestCase):
    def test_charter_has_measurable_loop_and_truth_separation(self):
        data = json.loads(CHARTER.read_text(encoding="utf-8"))
        self.assertEqual(data["schema"], "IMA-DISCOVERY-LOOP-1.0")
        self.assertIn("MEASURE", data["loop"])
        self.assertIn("TRY_TO_DISPROVE", data["loop"])
        self.assertGreaterEqual(len(data["measurement"]["required_metrics"]), 5)
        statuses = {item["status"] for item in data["initial_hypotheses"]}
        self.assertIn("OPEN_HYPOTHESIS", statuses)
        self.assertIn("SUPPORTED", statuses)

if __name__ == "__main__":
    unittest.main()
