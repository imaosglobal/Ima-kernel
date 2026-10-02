import unittest
from ima_runtime.development_journal import now_utc, record


class DevelopmentJournalTests(unittest.TestCase):
    def test_timestamp_is_iso8601(self):
        value = now_utc()
        self.assertIn("T", value)
        self.assertTrue(value.endswith("+00:00"))

    def test_record_has_timestamp_and_provenance(self):
        entry = record("TEST", "journal test", source="unit-test", status="VERIFIED")
        self.assertTrue(entry["timestamp"])
        self.assertEqual(entry["source"], "unit-test")
        self.assertEqual(entry["status"], "VERIFIED")


if __name__ == "__main__":
    unittest.main()
