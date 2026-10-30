import os
import tempfile
import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "ima_universal_interaction_memory_test_target",
    ROOT / ".ima" / "memory" / "universal_interaction_memory.py",
)
if spec is None or spec.loader is None:
    raise ImportError("memory runtime unavailable")
memory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(memory)


class UniversalMemoryContractTests(unittest.TestCase):
    def test_consent_is_required_and_export_delete_are_user_scoped(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = str(Path(tmp) / "memory.sqlite3")
            old_db = os.environ.get("PUBLIC_MEMORY_DB")
            os.environ["PUBLIC_MEMORY_DB"] = db
            try:
                memory.set_consent("user-a", "GRANTED", source="test")
                record = memory.capture(
                    user_id="user-a",
                    source="test",
                    content="private interaction",
                    consent="GRANTED",
                    interface="test",
                    status="EXECUTED",
                )
                self.assertTrue(memory.verify_user_memory("user-a")["verified"])
                self.assertEqual(len(memory.export_user_memory("user-a")), 1)
                self.assertEqual(memory.export_user_memory("user-b"), [])
                self.assertEqual(memory.delete_user_memory("user-a"), 1)
                self.assertEqual(memory.export_user_memory("user-a"), [])
                self.assertEqual(memory.get_consent("user-a")["status"], "GRANTED")
                self.assertTrue(record["id"])
            finally:
                if old_db is None:
                    os.environ.pop("PUBLIC_MEMORY_DB", None)
                else:
                    os.environ["PUBLIC_MEMORY_DB"] = old_db

    def test_capture_rejects_non_granted_consent_and_secret_like_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["PUBLIC_MEMORY_DB"] = str(Path(tmp) / "memory.sqlite3")
            try:
                memory.set_consent("user-a", "DENIED", source="test")
                with self.assertRaises(ValueError):
                    memory.capture(
                        user_id="user-a",
                        source="test",
                        content="should not persist",
                        consent="GRANTED",
                    )
                memory.set_consent("user-a", "GRANTED", source="test")
                with self.assertRaises(ValueError):
                    memory.capture(
                        user_id="user-a",
                        source="test",
                        content="api_key=super-secret",
                        consent="GRANTED",
                    )
            finally:
                os.environ.pop("PUBLIC_MEMORY_DB", None)


if __name__ == "__main__":
    unittest.main()
