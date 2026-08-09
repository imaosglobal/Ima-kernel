import importlib.util

spec = importlib.util.spec_from_file_location(
    "memory_policy",
    ".ima/runtime/memory_policy.py"
)

m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

result = m.evaluate(
    "identity",
    {"message":"IMA identity memory test"}
)

assert "type" in result
assert "importance" in result
assert result["type"] == "long_term"
assert result["importance"] >= 5

print("MEMORY POLICY V1 CONTRACT OK")
