import unittest

from ima_runtime.epistemic_state import build_epistemic_record


class EpistemicDecisionRecordTest(unittest.TestCase):
    def test_unknown_is_safe_default(self):
        record = build_epistemic_record("claim")
        self.assertEqual(record["truth_state"], "UNKNOWN")
        self.assertTrue(record["test"])

    def test_verified_evidence_can_promote_fact(self):
        record = build_epistemic_record("claim", evidence=["source"], context={"verified": True})
        self.assertEqual(record["truth_state"], "ESTABLISHED_FACT")

    def test_evidence_without_verification_is_supported_finding(self):
        record = build_epistemic_record("claim", evidence=["source"])
        self.assertEqual(record["truth_state"], "SUPPORTED_FINDING")

    def test_explicit_hypothesis_and_human_agency_fields(self):
        record = build_epistemic_record(
            "claim",
            context={
                "truth_state": "OPEN_HYPOTHESIS",
                "hypothesis": "H",
                "meaning": "M",
                "human_choice": "C",
                "feedback": ["F"],
                "learning": "L",
            },
        )
        self.assertEqual(record["truth_state"], "OPEN_HYPOTHESIS")
        self.assertEqual(record["human_choice"], "C")
        self.assertEqual(record["feedback"], ["F"])


if __name__ == "__main__":
    unittest.main()
