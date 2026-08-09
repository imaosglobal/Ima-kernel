import importlib.util

spec = importlib.util.spec_from_file_location(
    "memory_bus_v2",
    ".ima/runtime/memory_bus_v2.py"
)

m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

assert m.status()["memory_bus_v2"] is True

m.remember(
    "contract_test",
    {"status": "ok"}
)

result = m.recall("contract_test")

assert len(result) > 0
assert result[-1]["data"]["status"] == "ok"

print("MEMORY BUS V2 CONTRACT OK")
