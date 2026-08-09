from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone

ROOT = Path(".")
IMA = ROOT / ".ima"
AUTH = IMA / "CANONICAL_AUTHORITY"

timestamp = datetime.now(timezone.utc).isoformat()

EXCLUDE = {
    ".ima/self_repair/snapshots",
    ".ima/canonical_snapshots",
    ".ima/runtime_snapshots",
    ".ima/REPAIR_BACKUPS"
}

report = {
    "time": timestamp,
    "changed": [],
    "skipped_history": [],
    "found_direct_policy_reads": []
}


def excluded(path):
    s = str(path)
    return any(s.startswith(x) for x in EXCLUDE)


loader_import = """
from pathlib import Path
import sys

sys.path.insert(
    0,
    str(Path('.ima/CANONICAL_AUTHORITY'))
)

from policy_loader import load_root_policy

ROOT_POLICY = load_root_policy()
"""


for py in ROOT.rglob("*.py"):

    if excluded(py):
        report["skipped_history"].append(str(py))
        continue

    try:
        text = py.read_text(encoding="utf-8")
    except:
        continue

    if (
        "guardian/policy.json" in text
        or "universal_human_flourishing_policy.json" in text
    ):

        report["found_direct_policy_reads"].append(str(py))

        if "load_root_policy" not in text:

            backup = py.with_suffix(
                py.suffix + ".before_root_policy"
            )

            backup.write_text(
                text,
                encoding="utf-8"
            )

            text = loader_import + "\n\n" + text

            text = text.replace(
                'Path(".ima/guardian/policy.json")',
                'Path(".ima/CANONICAL_AUTHORITY/root_policy.json")'
            )

            text = text.replace(
                'Path(".ima/policy/universal_human_flourishing_policy.json")',
                'Path(".ima/CANONICAL_AUTHORITY/root_policy.json")'
            )

            py.write_text(
                text,
                encoding="utf-8"
            )

            report["changed"].append(str(py))


# create compile policy

policy = AUTH / "compile_policy.json"

policy.write_text(
    json.dumps(
        {
            "compile_policy": {
                "ignore_historical_backups": True,
                "ignore_snapshots": True,
                "ignore_repair_archives": True,
                "strict_runtime_only": True
            }
        },
        indent=2
    ),
    encoding="utf-8"
)


(Path(".ima/CANONICAL_AUTHORITY/root_connection_report.json")
 .write_text(
    json.dumps(report, indent=2),
    encoding="utf-8"
))


print("CANONICAL CONNECTION COMPLETE")
print("changed:", len(report["changed"]))
print("history skipped:", len(report["skipped_history"]))
print("direct reads found:", len(report["found_direct_policy_reads"]))
print("report:")
print(".ima/CANONICAL_AUTHORITY/root_connection_report.json")

