import unittest

from learning.industry_pattern_adapter import adapt_domain, adapt_domains


class IndustryPatternAdapterTests(unittest.TestCase):
    def test_known_domain_gets_canonical_patterns(self):
        rows = adapt_domain("plumbing")
        self.assertTrue(rows)
        self.assertTrue(any(row["pattern"] == "field_service" for row in rows))

    def test_unknown_domain_uses_safe_generic_patterns(self):
        rows = adapt_domain("new_future_sector")
        self.assertTrue(rows)
        self.assertTrue(any(row["pattern"] == "privacy_boundary" for row in rows))

    def test_transaction_patterns_require_approval(self):
        rows = adapt_domain("finance")
        transaction = [r for r in rows if r["pattern"] == "transaction_lifecycle"]
        self.assertEqual(len(transaction), 1)
        self.assertTrue(transaction[0]["requires_approval"])

    def test_batch_adaptation(self):
        rows = adapt_domains(["3d_games", "marketing", "plumbing"])
        self.assertGreaterEqual(len(rows), 6)


if __name__ == "__main__":
    unittest.main()
