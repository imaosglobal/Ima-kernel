import json
import time
import subprocess
from pathlib import Path

def exists(path):
    return Path(path).exists()

def check_system():
    return {
        "gateway": exists(
            "product/gateway/product_gateway.py"
        ),
        "health": exists(
            "product/health/health_manager.py"
        ),
        "device": exists(
            "product/device/device_manager.py"
        ),
        "update": exists(
            "product/update/update_manager.py"
        ),
        "api": exists(
            "api/server.py"
        )
    }

def launch_status():
    checks = check_system()

    return {
        "product": "IMA",
        "status": "READY"
            if all(checks.values())
            else "INCOMPLETE",
        "components": checks,
        "time": time.time()
    }

if __name__ == "__main__":
        launch_status(),
        indent=2
    ))
