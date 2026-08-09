import importlib.util

POLICY_PATH = ".ima/runtime/memory_policy.py"
ADAPTER_PATH = ".ima/runtime/memory_bus_adapter.py"

spec = importlib.util.spec_from_file_location(
    "memory_policy",
    POLICY_PATH
)
memory_policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(memory_policy)


spec = importlib.util.spec_from_file_location(
    "memory_bus_adapter",
    ADAPTER_PATH
)
memory_bus_adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(memory_bus_adapter)


def remember(event_type, data):
    policy = memory_policy.evaluate(event_type, data)

    payload = {
        "policy": policy,
        "data": data
    }

    return memory_bus_adapter.send(
        event_type,
        payload
    )


def health():
    return {
        "policy": True,
        "adapter": memory_bus_adapter.health()
    }
