import unittest

from learning.competitive_advantage_engine import CompetitiveLesson, normalize_lessons, rank_lessons


class CompetitiveAdvantageEngineTests(unittest.TestCase):
    def test_normalizes_evidence_bounded_lesson(self):
        item = CompetitiveLesson(
            "Google Gemini", "persistent_context", "one context across devices",
            "public product documentation", "IMA needs live verification",
            "benchmark and adapt the pattern through canonical runtime",
            "less re-briefing and better continuity",
        )
        rows = normalize_lessons([item])
        self.assertEqual(rows[0]["status"], "REVIEW_REQUIRED")

    def test_ranks_durable_capabilities_first(self):
        a = CompetitiveLesson("A", "benchmarking", "x", "e", "g", "a", "u")
        b = CompetitiveLesson("B", "universal_access", "x", "e", "g", "a", "u")
        rows = rank_lessons([a, b])
        self.assertEqual(rows[0]["competitor"], "B")

    def test_rejects_missing_evidence(self):
        with self.assertRaises(ValueError):
            normalize_lessons([CompetitiveLesson("A", "research", "x", "", "g", "a", "u")])


if __name__ == "__main__":
    unittest.main()
