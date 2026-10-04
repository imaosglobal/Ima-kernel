import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / ".ima" / "plugins" / "capability_runtime.py"
spec = importlib.util.spec_from_file_location("ima_capability_runtime_test", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CapabilityRuntimeTests(unittest.TestCase):
    def test_snapshot_connects_registry_and_gap_queue(self):
        snapshot = module.snapshot()
        self.assertEqual(snapshot["schema"], "IMA-CAPABILITY-RUNTIME-1.0")
        self.assertIn("providers", snapshot)
        self.assertIn("next_gap", snapshot)
        self.assertIn("gap_snapshot", snapshot)

    def test_connected_capability_routes(self):
        result = module.route("image_generation")
        self.assertTrue(result["available"])
        self.assertTrue(result["execution_allowed"])
        self.assertEqual(result["truth_state"], "connected")

    def test_unknown_capability_is_not_claimed(self):
        result = module.route("imaginary_unverified_capability")
        self.assertFalse(result["available"])
        self.assertFalse(result["execution_allowed"])
        self.assertIsNone(result["route"])


if __name__ == "__main__":
    unittest.main()
