from ima_runtime.reflection_gap_closure import Conclusion, compare, close_gaps, self_test


def test_agreement_has_no_gap():
    a = Conclusion("x", ("e",), uncertainty="low", proposed_next_step="verify")
    assert compare(a, a).gap_types == ()


def test_disagreement_is_explicit():
    a = Conclusion("x", ("e1",), uncertainty="low", proposed_next_step="verify")
    b = Conclusion("y", ("e2",), uncertainty="low", proposed_next_step="verify")
    r = compare(a, b)
    assert not r.agreement
    assert "EVIDENCE_GAP" in r.gap_types
    assert r.resolution_status == "UNRESOLVED"


def test_missing_independent_is_unknown_not_agreement():
    a = Conclusion("x", ("e",))
    r = compare(a, None)
    assert not r.agreement
    assert r.gap_types == ("TRUE_UNKNOWN",)


def test_verified_closure_requires_evidence():
    a = Conclusion("x", ("e1",))
    b = Conclusion("y", ("e2",))
    r = compare(a, b)
    unresolved = close_gaps(r, lambda _comparison, _gap: False)
    assert unresolved.resolution_status == "UNRESOLVED"
    resolved = close_gaps(r, lambda _comparison, gap: gap == "EVIDENCE_GAP")
    assert resolved.resolution_status == "RESOLVED"
    assert resolved.gap_types == ()


def test_context_gap_types():
    a = Conclusion("x", ("e",), assumptions=("a",), objective="o1", scope="s1", capability="c1", values=("v1",), uncertainty="u1")
    b = Conclusion("x", ("e",), assumptions=("b",), objective="o2", scope="s2", capability="c2", values=("v2",), uncertainty="u2")
    r = compare(a, b)
    assert {"ASSUMPTION_GAP", "OBJECTIVE_GAP", "SCOPE_GAP", "CAPABILITY_GAP", "VALUE_GAP", "UNCERTAINTY_GAP"} <= set(r.gap_types)


def test_self_test():
    assert self_test()["ok"] is True
