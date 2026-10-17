import unittest

from core.human_culture import (
    CULTURAL_DOMAINS,
    CULTURAL_EPISTEMIC_CLASSES,
    CULTURE_POLICY_VERSION,
    FOUNDATIONAL_PHRASE,
    SYSTEM_CONTEXT,
    culture_contract,
    culture_context,
    validate_culture_contract,
)


class HumanCultureTests(unittest.TestCase):
    def test_contract_is_valid(self):
        result = validate_culture_contract()
        self.assertTrue(result["valid"], result)
        self.assertTrue(CULTURE_POLICY_VERSION)

    def test_preserves_many_cultures_without_homogenization(self):
        self.assertIn("one humanity, many cultures, shared memory, shared future", culture_contract()["principles"])
        self.assertIn("Do not replace, erase, rank, appropriate, or silently homogenize", SYSTEM_CONTEXT)
        self.assertGreaterEqual(len(CULTURAL_DOMAINS), 10)

    def test_preserves_epistemic_distinctions(self):
        for item in (
            "primary_evidence",
            "cultural_memory",
            "mythic_or_theological_tradition",
            "scholarly_interpretation",
            "hypothesis",
            "unknown_or_disputed",
        ):
            self.assertIn(item, CULTURAL_EPISTEMIC_CLASSES)

    def test_founder_is_not_authority(self):
        self.assertIn("founder", SYSTEM_CONTEXT.lower())
        self.assertIn("permanent authority", SYSTEM_CONTEXT)
        self.assertEqual(culture_contract()["founder_role"], "initiator_only")
        self.assertEqual(culture_contract()["ima_role"], "infrastructure_not_sovereign")

    def test_context_is_available_to_model_pipeline(self):
        self.assertEqual(culture_context(), SYSTEM_CONTEXT)
        self.assertIn(FOUNDATIONAL_PHRASE, culture_context())


if __name__ == "__main__":
    unittest.main()
