import unittest
from core.global_humanitarian_intelligence import (
    WorldObservation, classify_text, build_humanitarian_plan,
    analyze_observation, should_enter_world_pulse
)

class GlobalHumanitarianIntelligenceTests(unittest.TestCase):
    def test_classifies_conflict_and_disaster(self):
        self.assertEqual(classify_text("armed conflict and bombing"), "CONFLICT")
        self.assertEqual(classify_text("earthquake and flood"), "DISASTER")

    def test_plan_is_nonviolent_and_agency_preserving(self):
        plan = build_humanitarian_plan("CONFLICT")
        self.assertIn("SUPPORT_NONVIOLENT_DIALOGUE", plan.nonviolent_actions)
        self.assertEqual(plan.agency_rule, "INFORM_AND_CONNECT; DO_NOT_DECIDE_FOR_PEOPLE")

    def test_analysis_does_not_turn_classification_into_fact(self):
        obs = WorldObservation(
            title="Reported unrest",
            event_type="UNKNOWN",
            place="Example",
            observed_at="2026-11-06T00:00:00Z",
            source_url="https://example.org/report",
            source_name="example",
            summary="reported protest",
        )
        result = analyze_observation(obs)
        self.assertTrue(result["classification"]["classification_is_not_fact"])
        self.assertEqual(result["external_action"]["status"], "HUMAN_AUTHORIZATION_REQUIRED")

    def test_world_pulse_trigger(self):
        self.assertTrue(should_enter_world_pulse("מה קורה עכשיו במלחמה?"))
        self.assertTrue(should_enter_world_pulse("What is happening in the world?"))
        self.assertFalse(should_enter_world_pulse("write me a poem"))

if __name__ == "__main__":
    unittest.main()
