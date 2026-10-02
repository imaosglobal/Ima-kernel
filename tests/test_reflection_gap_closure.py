from ima_runtime.reflection_gap_closure import Conclusion, compare, self_test

def test_agreement_has_no_gap():
    a=Conclusion("x",("e",),(),"low","verify")
    assert compare(a,a).gap_types==()

def test_disagreement_is_explicit():
    a=Conclusion("x",("e1",),(),"low","verify")
    b=Conclusion("y",("e2",),(),"low","verify")
    r=compare(a,b)
    assert not r.agreement
    assert "EVIDENCE_GAP" in r.gap_types
    assert r.resolution_status=="UNRESOLVED"

def test_self_test():
    assert self_test()["ok"] is True
