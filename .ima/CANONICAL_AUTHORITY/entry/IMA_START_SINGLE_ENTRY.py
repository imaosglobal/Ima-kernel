"""Canonical IMA entry self-verification.

The entry remains intentionally small: it verifies that the reflection runtime can load and execute.
"""
from ima_runtime.reflection_gap_closure import self_test as reflection_self_test
from ima_runtime.zero_point_encounter import self_test as zero_point_self_test

print("IMA START")
reflection = reflection_self_test()
zero_point = zero_point_self_test()
print("IMA REFLECTION GAP-CLOSURE SELF-TEST:", "PASS" if reflection["ok"] else "FAIL")
print("IMA ZERO-POINT ENCOUNTER SELF-TEST:", "PASS" if zero_point["ok"] else "FAIL")
