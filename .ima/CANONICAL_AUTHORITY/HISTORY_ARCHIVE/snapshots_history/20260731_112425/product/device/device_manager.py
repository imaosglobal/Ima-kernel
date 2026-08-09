import platform
import time

def device_info():
    return {
        "platform": platform.system(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "time": time.time()
    }

def capabilities():
    return {
        "network": True,
        "storage": True,
        "sensors": "unknown",
        "bluetooth": "unknown"
    }
