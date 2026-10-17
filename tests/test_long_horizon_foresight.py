import unittest
from core.long_horizon_foresight import HORIZONS, create_trajectory, trajectory_packet

class ForesightTests(unittest.TestCase):
    def test_multiple_horizons_exist(self):
        self.assertEqual(HORIZONS[0].label, "NOW")
        self.assertIn("ONE_YEAR", [h.label for h in HORIZONS])
        self.assertIn("TEN_YEARS", [h.label for h in HORIZONS])

    def test_future_is_hypothesis_and_has_present_actions(self):
        t=create_trajectory(HORIZONS[2], "more autonomous capability discovery", prerequisites=["verified tools"], signals=["new accessible tools"], first_actions=["audit capability registry"])
        p=trajectory_packet(t)
        self.assertEqual(p["confidence"], "HYPOTHESIS")
        self.assertTrue(p["first_actions"])
        self.assertIn("safe present action", p["rule"])

if __name__ == "__main__":
    unittest.main()
