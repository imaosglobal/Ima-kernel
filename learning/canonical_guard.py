from pathlib import Path
import json

CANONICAL=json.loads(
Path(".ima/governance/CANONICAL_MAP.json").read_text()
)

def check(path):

    forbidden=[
        "new_brain",
        "new_orchestrator",
        "another_kernel"
    ]

    for x in forbidden:
        if x in path.lower():
            raise RuntimeError(
f"""
IMA BLOCKED DUPLICATE

Use existing canonical:
{CANONICAL}
"""
)

    return True
