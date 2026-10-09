import unittest

from ima_trend_engine import (
    DIMENSIONS,
    assess_demand,
    build_opportunity_brief,
    score_opportunity,
    validate_signal,
)


def signal(url, kind="social_mention", captured_at="2026-10-09T10:00:00Z"):
    return {
        "source_url": url,
        "captured_at": captured_at,
        "market": "IL",
        "language": "he",
        "kind": kind,
        "summary": "Example evidence supplied for a unit test",
        "sample_size": 12,
    }


class TrendEngineTests(unittest.TestCase):
    def test_rejects_timestamp_without_timezone(self):
        errors = validate_signal(signal("https://example.com/post", captured_at="2026-10-09T10:00:00"))
        self.assertTrue(any("timezone" in error for error in errors))

    def test_invalid_score_value_fails_closed(self):
        with self.assertRaises(ValueError):
            score_opportunity({"trend_acceleration": 6, "demand_persistence": 3,
                               "audience_relevance": 3, "purchase_intent": 3,
                               "unmet_need": 3})

    def test_insufficient_dimensions_are_not_scored(self):
        result = score_opportunity({"trend_acceleration": 5, "demand_persistence": 4})
        self.assertIsNone(result["score"])
        self.assertEqual(result["recommendation"], "collect_more_evidence")

    def test_score_uses_only_present_dimensions(self):
        result = score_opportunity({name: 4 for name in DIMENSIONS[:5]})
        self.assertEqual(result["score"], 80.0)
        self.assertEqual(result["dimensions_scored"], 5)
        self.assertEqual(result["recommendation"], "test_small")

    def test_one_domain_cannot_validate_demand(self):
        result = assess_demand([
            signal("https://a.example.com/one"),
            signal("https://a.example.com/two", "purchase_intent"),
            signal("https://a.example.com/three"),
        ])
        self.assertEqual(result["status"], "DISCOVERED")

    def test_multiple_domains_and_purchase_intent_can_meet_threshold(self):
        result = assess_demand([
            signal("https://alpha.example/one"),
            signal("https://beta.example/two", "purchase_intent"),
            signal("https://gamma.example/three"),
        ])
        self.assertEqual(result["status"], "VALIDATED")
        self.assertEqual(result["independent_domain_count"], 3)

    def test_brief_never_claims_commercial_success(self):
        brief = build_opportunity_brief(
            title="Test", customer_problem="A test problem", market="IL",
            dimensions={name: 4 for name in DIMENSIONS[:5]},
            signals=[signal("https://alpha.example/1"),
                     signal("https://beta.example/2", "purchase_intent"),
                     signal("https://gamma.example/3")],
        )
        self.assertEqual(brief["commercial_state"], "NOT_ESTABLISHED")
        self.assertEqual(brief["evidence_state"], "VALIDATED")


if __name__ == "__main__":
    unittest.main()
