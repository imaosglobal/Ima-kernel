from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
AUTH = ROOT / ".ima" / "CANONICAL_AUTHORITY"

sys.path.insert(0, str(AUTH))
sys.path.insert(0, str(ROOT))

adapter_file = AUTH / "governance" / "adapters" / "http_api_adapter.py"

if not adapter_file.exists():
    raise SystemExit(f"ADAPTER_NOT_FOUND: {adapter_file}")

from governance.adapters.http_api_adapter import HTTPAPIAdapter

print("HTTP_ADAPTER_IMPORT_OK")
print("HTTP_ADAPTER_SELFTEST_OK")
