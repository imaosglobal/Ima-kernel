import tempfile
import unittest
from pathlib import Path
import public_memory
from importlib.util import spec_from_file_location, module_from_spec

ROOT = Path(__file__).resolve().parents[1]
runtime_path = ROOT / ".ima/memory/universal_interaction_memory.py"
adapter_path = ROOT / ".ima/ima_canonical_memory_adapter.py"


class CanonicalMemoryAdapterTests(unittest.TestCase):
    def test_adapter_persists_through_canonical_runtime(self):
        with tempfile.TemporaryDirectory() as td:
            old = public_memory._DB
            public_memory._DB = Path(td) / "m.sqlite3"
            try:
                spec = spec_from_file_location("canonical_adapter", adapter_path)
                adapter = module_from_spec(spec)
                assert spec and spec.loader
                spec.loader.exec_module(adapter)
                adapter._MODULE.set_consent("u", "GRANTED")
                result = adapter.save_memory({
                    "user_id": "u",
                    "source": "chat",
                    "content": "hello",
                    "consent": "GRANTED",
                })
                self.assertEqual(result["schema"], "IMA-UNIVERSAL-INTERACTION-MEMORY-1.1")
                self.assertEqual(len(adapter._MODULE.export_user_memory("u")), 1)
            finally:
                public_memory._DB = old

    def test_adapter_rejects_consent_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            old = public_memory._DB
            public_memory._DB = Path(td) / "m.sqlite3"
            try:
                spec = spec_from_file_location("canonical_adapter", adapter_path)
                adapter = module_from_spec(spec)
                assert spec and spec.loader
                spec.loader.exec_module(adapter)
                with self.assertRaises(ValueError):
                    adapter.save_memory({
                        "user_id": "u",
                        "source": "chat",
                        "content": "hello",
                        "consent": "GRANTED",
                    })
            finally:
                public_memory._DB = old


if __name__ == "__main__":
    unittest.main()
