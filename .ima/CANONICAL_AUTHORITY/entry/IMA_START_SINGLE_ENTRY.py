"""Canonical IMA entry self-verification.

The entry remains intentionally small: it verifies that the reflection runtime can load and execute.
"""
from ima_runtime.reflection_gap_closure import self_test

print("IMA START")
result = self_test()
print("IMA REFLECTION GAP-CLOSURE SELF-TEST:", "PASS" if result["ok"] else "FAIL")
