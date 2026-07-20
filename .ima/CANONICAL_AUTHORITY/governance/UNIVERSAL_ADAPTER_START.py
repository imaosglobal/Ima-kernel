import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".ima"))

from CANONICAL_AUTHORITY.governance.UNIVERSAL_ADAPTER_ROUTER import UniversalAdapterRouter

REGISTRY = ROOT / ".ima/CANONICAL_AUTHORITY/governance/UNIVERSAL_ADAPTER_REGISTRY.json"

router = UniversalAdapterRouter(REGISTRY)

target = "https://example.com"

action = {
    "url": target,
    "method": "GET",
    "headers": {}
}

result = router.execute(target, action)

print(json.dumps(result, indent=2))
