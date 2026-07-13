import json
import time
from pathlib import Path

def check_file(path):
    return Path(path).exists()

def health_report():
    checks = {
        "core": {
            "conversation_layer": check_file("conversation_layer.py"),
            "runtime": check_file("ima_master_runtime.py"),
            "start": check_file("IMA_START.py")
        },
        "gateway": {
            "product_gateway": check_file(
                "product/gateway/product_gateway.py"
            )
        },
        "clients": {
            "web": check_file("product/clients/web/client.json"),
            "android": check_file("product/clients/android/client.json"),
            "mobile": check_file("product/clients/mobile/client.json")
        },
        "device": {
            "manager": check_file(
                "product/device/device_manager.py"
            )
        },
        "update": {
            "manager": check_file(
                "product/update/update_manager.py"
            )
        },
        "time": time.time()
    }

    checks["status"] = (
        "READY"
        if all(
            v is True
            for group in checks.values()
            if isinstance(group, dict)
            for v in group.values()
        )
        else "INCOMPLETE"
    )

    return checks


def save_report():
    report = health_report()
    p = Path(".ima/reports/product_health_report.json")
    p.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )
    return report
