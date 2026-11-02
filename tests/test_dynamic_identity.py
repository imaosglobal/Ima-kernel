import unittest

from core.dynamic_identity import (
    DYNAMIC_IDENTITY_CONTEXT,
    dynamic_identity_contract,
    dynamic_identity_context,
)
from core.human_intelligence import POLICY_VERSION, compose_prompt
from core.ima_loop import loop_contract, loop_context
from ima_mom import generate_answer


class DynamicIdentityTests(unittest.TestCase):
    def test_dynamic_identity_contract_is_explicit(self):
        contract = dynamic_identity_contract()
        self.assertTrue(contract["continuity_and_becoming"])
        self.assertTrue(contract["multiple_states_without_reduction"])
        self.assertTrue(contract["inner_outer_distinction"])
        self.assertTrue(contract["connect_or_differentiate_contextually"])
        self.assertTrue(contract["preserve_unresolved_contradictions"])
        self.assertTrue(contract["past_is_not_destiny"])
        self.assertTrue(contract["user_can_correct_or_reject_interpretations"])
        self.assertTrue(contract["private_by_default"])
        self.assertTrue(contract["shared_learning_requires_authorization"])
        self.assertTrue(contract["universal_consciousness_is_not_asserted"])

    def test_provider_prompt_includes_dynamic_identity_policy(self):
        prompt = compose_prompt("Who am I?")
        self.assertEqual(POLICY_VERSION, "human-intelligence-v1.4")
        self.assertIn("DYNAMIC HUMAN IDENTITY, MULTIPLICITY", prompt)
        self.assertIn("both continuity and becoming", prompt)
        self.assertIn("Do not force unity", prompt)
        self.assertIn("USER MESSAGE", prompt)

    def test_unified_loop_exposes_dynamic_identity(self):
        contract = loop_contract()
        self.assertTrue(contract["dynamic_identity"]["continuity_and_becoming"])
        self.assertTrue(contract["identity"]["multiple_states_without_reduction"])
        self.assertIn("DISTINGUISH_INNER_OUTER", contract["stages"])
        self.assertIn("PRESERVE_UNRESOLVED", contract["stages"])
        self.assertIn("HOLD MULTIPLICITY", loop_context())

    def test_fallback_identity_answer_does_not_fix_a_single_identity(self):
        answer = generate_answer("מי אני?", {"qa": []})
        self.assertIn("רצף מתמשך", answer)
        self.assertIn("משתנה", answer)
        self.assertIn("אינך מצטמצם", answer)

    def test_poetic_unity_is_not_presented_as_scientific_fact(self):
        self.assertIn("metaphor", DYNAMIC_IDENTITY_CONTEXT.lower())
        self.assertIn("not an established scientific claim", DYNAMIC_IDENTITY_CONTEXT)
        self.assertTrue(dynamic_identity_contract()["universal_consciousness_is_not_asserted"])


if __name__ == "__main__":
    unittest.main()
