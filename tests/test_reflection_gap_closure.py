import unittest

from ima_runtime.reflection_gap_closure import Conclusion, compare, close_gaps, self_test


class ReflectionGapClosureTests(unittest.TestCase):
    def test_agreement_has_no_gap(self):
        a = Conclusion("x", ("e",), uncertainty="low", proposed_next_step="verify")
        self.assertEqual(compare(a, a).gap_types, ())

    def test_disagreement_is_explicit(self):
        a = Conclusion("x", ("e1",), uncertainty="low", proposed_next_step="verify")
        b = Conclusion("y", ("e2",), uncertainty="low", proposed_next_step="verify")
        r = compare(a, b)
        self.assertFalse(r.agreement)
        self.assertIn("EVIDENCE_GAP", r.gap_types)
        self.assertEqual(r.resolution_status, "UNRESOLVED")

    def test_missing_independent_is_unknown_not_agreement(self):
        a = Conclusion("x", ("e",))
        r = compare(a, None)
        self.assertFalse(r.agreement)
        self.assertEqual(r.gap_types, ("TRUE_UNKNOWN",))

    def test_verified_closure_requires_evidence(self):
        a = Conclusion("x", ("e1",))
        b = Conclusion("y", ("e2",))
        r = compare(a, b)
        unresolved = close_gaps(r, lambda _comparison, _gap: False)
        self.assertEqual(unresolved.resolution_status, "UNRESOLVED")
        resolved = close_gaps(r, lambda _comparison, gap: gap == "EVIDENCE_GAP")
        self.assertEqual(resolved.resolution_status, "RESOLVED")
        self.assertEqual(resolved.gap_types, ())

    def test_context_gap_types(self):
        a = Conclusion("x", ("e",), assumptions=("a",), objective="o1", scope="s1", capability="c1", values=("v1",), uncertainty="u1")
        b = Conclusion("x", ("e",), assumptions=("b",), objective="o2", scope="s2", capability="c2", values=("v2",), uncertainty="u2")
        r = compare(a, b)
        self.assertTrue({"ASSUMPTION_GAP", "OBJECTIVE_GAP", "SCOPE_GAP", "CAPABILITY_GAP", "VALUE_GAP", "UNCERTAINTY_GAP"} <= set(r.gap_types))

    def test_self_test(self):
        self.assertTrue(self_test()["ok"])


if __name__ == "__main__":
    unittest.main()
