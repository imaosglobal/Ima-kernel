import unittest

from ima_runtime.reflection_runtime import reflect


class ReflectionEpistemicIntegrationTest(unittest.TestCase):
    def test_reflection_emits_epistemic_record(self):
        record = reflect(
            "A claim without evidence",
            context={"scope": "test", "uncertainty": "unknown"},
        )
        self.assertEqual(record["epistemic"]["schema"], "IMA-EPISTEMIC-DECISION-1.0")
        self.assertEqual(record["epistemic"]["truth_state"], "UNKNOWN")
        self.assertTrue(record["epistemic"]["test"])


if __name__ == "__main__":
    unittest.main()
