import json
from pathlib import Path

CONFIG = json.loads(
    Path(__file__).with_name("client_config.json").read_text()
)

def config():
    return CONFIG

def health():
    return {
        "client": True,
        "gateway": CONFIG["gateway"],
        "status": "READY"
    }

if __name__ == "__main__":
    print(json.dumps(health(), indent=2))
