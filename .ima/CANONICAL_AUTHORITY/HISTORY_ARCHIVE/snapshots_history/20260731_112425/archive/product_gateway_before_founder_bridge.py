import time

try:
    import ima_master_runtime
except Exception:
    ima_master_runtime = None


def ask(message):
    if ima_master_runtime:
        return ima_master_runtime.ask(message)

    return {
        "status": "fallback",
        "message": message
    }


def health():
    return {
        "product_gateway": True,
        "runtime_connected": ima_master_runtime is not None,
        "time": time.time()
    }
