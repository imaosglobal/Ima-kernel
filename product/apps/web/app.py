import json
from pathlib import Path

from product.apps.shared.gateway_client import health

CONFIG=json.loads(
    Path(__file__).with_name("web_config.json").read_text()
)

def status():
    return {
        "client": CONFIG["platform"],
        "config": CONFIG,
        "sdk": health()
    }

if __name__=="__main__":
    print(json.dumps(status(), indent=2))
