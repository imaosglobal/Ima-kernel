import json
import tempfile
import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / ".ima" / "web_intelligence" / "global_discovery.py"

spec = importlib.util.spec_from_file_location("ima_global_discovery", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class WebIntelligenceTests(unittest.TestCase):
    def test_digest_is_stable(self):
        self.assertEqual(mod.digest("IMA"), mod.digest("IMA"))
        self.assertNotEqual(mod.digest("IMA"), mod.digest("ima"))

    def test_add_rejects_credentials(self):
        items = []
        mod.add(items, "https://user:pass@example.com/a", "bad", "x", "feed")
        self.assertEqual(items, [])

    def test_state_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            old = mod.STATE
            try:
                mod.STATE = Path(td) / "state.json"
                state = {"schema": "test", "seen": {}, "last_run": None}
                mod.save_state(state)
                self.assertEqual(mod.load_state(), state)
            finally:
                mod.STATE = old


if __name__ == "__main__":
    unittest.main()
