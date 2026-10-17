import unittest
from core.long_horizon_foresight import (
    HORIZONS,
    create_trajectory,
    prioritize_actions,
    re_evaluation_plan,
    system_foresight,
    trajectory_packet,
)


class ForesightTests(unittest.TestCase):
    def test_multiple_horizons_exist(self):
        self.assertEqual(HORIZONS[0].label, "NOW")
        self.assertIn("ONE_YEAR", [h.label for h in HORIZONS])
        self.assertIn("TEN_YEARS", [h.label for h in HORIZONS])

    def test_future_is_hypothesis_and_has_present_actions(self):
        t = create_trajectory(
            HORIZONS[2],
            "more autonomous capability discovery",
            prerequisites=["verified tools"],
            signals=["new accessible tools"],
            first_actions=["audit capability registry"],
            tests=["run registry tests"],
            reevaluate_when=["new tool evidence"],
        )
        p = trajectory_packet(t)
        self.assertEqual(p["confidence"], "HYPOTHESIS")
        self.assertTrue(p["first_actions"])
        self.assertTrue(p["tests"])
        self.assertTrue(p["reevaluate_when"])
        self.assertTrue(p["not_prediction"])
        self.assertIn("test", p["rule"])

    def test_prioritize_actions_puts_now_before_year(self):
        trajectories = [
            create_trajectory(HORIZONS[2], "year", first_actions=["year action"]),
            create_trajectory(HORIZONS[0], "now", first_actions=["now action"]),
        ]
        actions = prioritize_actions(trajectories)
        self.assertEqual(actions[0]["action"], "now action")

    def test_re_evaluation_plan_is_explicit(self):
        t = create_trajectory(
            HORIZONS[1],
            "reliable capability",
            signals=["usage evidence"],
            reevaluate_when=["new evidence"],
        )
        plan = re_evaluation_plan(t)
        self.assertEqual(plan["signals_to_watch"], ["usage evidence"])
        self.assertIn("update prerequisites", plan["next_step"])

    def test_system_foresight_covers_every_component(self):
        result = system_foresight(["human intelligence", "global growth"])
        self.assertEqual(set(result), {"human intelligence", "global growth"})
        self.assertEqual(len(result["human intelligence"]), len(HORIZONS))
        for packet in result["global growth"]:
            self.assertTrue(packet["first_actions"])
            self.assertTrue(packet["tests"])
            self.assertTrue(packet["reevaluate_when"])


if __name__ == "__main__":
    unittest.main()
