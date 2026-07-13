import importlib.util

V2_PATH = ".ima/runtime/memory_bus_v2.py"

spec = importlib.util.spec_from_file_location(
    "memory_bus_v2",
    V2_PATH
)

memory_bus_v2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(memory_bus_v2)


def send(event_type, data):
    return memory_bus_v2.remember(
        event_type,
        data
    )


def search(keyword, limit=10):
    return memory_bus_v2.recall(
        keyword,
        limit
    )


def health():
    return memory_bus_v2.status()
