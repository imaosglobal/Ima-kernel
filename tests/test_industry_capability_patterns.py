import unittest

from learning.industry_capability_patterns import (
    INDUSTRY_DOMAINS,
    TRANSFERABLE_PATTERNS,
    normalize_candidates,
)


class IndustryCapabilityPatternsTests(unittest.TestCase):
    def test_taxonomy_is_unique_and_broad(self):
        self.assertEqual(len(INDUSTRY_DOMAINS), len(set(INDUSTRY_DOMAINS)))
        self.assertGreaterEqual(len(INDUSTRY_DOMAINS), 70)

    def test_core_transferable_patterns_exist(self):
        for key in ("workflow_orchestration", "diagnosis", "visual_spatial_reasoning",
                    "transaction_lifecycle", "human_approval", "privacy_boundary"):
            self.assertIn(key, TRANSFERABLE_PATTERNS)

    def test_unknown_domain_is_not_promoted(self):
        result = normalize_candidates([{
            "domain": "unknown_sector",
            "source": "x",
            "lesson": "y",
            "canonical_target": "z",
            "conflict_check": "c",
        }])
        self.assertEqual(result, [])

    def test_valid_candidate_is_reviewable(self):
        result = normalize_candidates([{
            "domain": "plumbing",
            "source": "example",
            "lesson": "field-service diagnosis",
            "canonical_target": "canonical workflow orchestration",
            "conflict_check": "no duplicate execution authority",
        }])
        self.assertEqual(result[0]["status"], "REVIEW_REQUIRED")


if __name__ == "__main__":
    unittest.main()
