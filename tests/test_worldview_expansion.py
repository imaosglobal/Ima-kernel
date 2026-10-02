import unittest

from ima_runtime.worldview_expansion import SourceResult, expand, self_test


class WorldviewExpansionTests(unittest.TestCase):
    def test_self_test(self):
        self.assertTrue(self_test())

    def test_unavailable_is_explicit(self):
        result = expand("test", [])
        self.assertIn("TRUE_UNKNOWN:NO_SOURCE_WAS_ACTUALLY_CONSULTED", result["gaps"])

    def test_provider_result_is_recorded(self):
        result = expand(
            "test",
            [("person-a", "human", lambda q: SourceResult("person-a", "human", "CONSULTED", ("claim",), ("direct",)))],
            required_kinds=("human",),
        )
        self.assertEqual(result["sources_consulted"], ["person-a"])
        self.assertFalse(result["gaps"])


if __name__ == "__main__":
    unittest.main()
