import unittest

from core.world_model_humanization import assess_world_model_use, world_model_context


class WorldModelHumanizationTests(unittest.TestCase):
    def test_simulation_is_not_reality(self):
        self.assertIn("simulations, not reality", world_model_context())

    def test_high_impact_use_requires_real_world_validation(self):
        result = assess_world_model_use("robot autonomous driving safety")
        self.assertTrue(result["high_impact"])
        self.assertTrue(result["real_world_validation_required"])
        self.assertTrue(result["human_override_required"])

    def test_ordinary_exploration_is_bounded(self):
        result = assess_world_model_use("explore a fictional city")
        self.assertFalse(result["high_impact"])
        self.assertEqual(result["status"], "SAFE_BOUNDED")


if __name__ == "__main__":
    unittest.main()
