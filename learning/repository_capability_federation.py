"""Canonical federation registry for capabilities discovered across IMA repositories.

This module does not create a second runtime or memory authority. It only maps
source capabilities to their canonical IMA subsystems and preserves provenance.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "docs" / "IMA_UNIFIED_REPOSITORY_CAPABILITY_MAP.json"


def load_repository_capability_map() -> dict:
    return json.loads(MAP.read_text(encoding="utf-8"))


def canonical_sources() -> dict:
    data = load_repository_capability_map()
    return {
        item["name"]: item["role"]
        for item in data["repositories"]
        if item["status"] == "AUTHORITATIVE"
    }


def capability_routes() -> list[dict]:
    data = load_repository_capability_map()
    return data["capability_mappings"]


def assert_no_parallel_authority() -> bool:
    data = load_repository_capability_map()
    authoritative = [
        x for x in data["repositories"]
        if x["status"] == "AUTHORITATIVE"
    ]
    return len(authoritative) == 1 and authoritative[0]["name"] == "imaosglobal/Ima-kernel"


if __name__ == "__main__":
    data = load_repository_capability_map()
    print(json.dumps({
        "canonical_repository": data["canonical_repository"],
        "repositories_mapped": len(data["repositories"]),
        "capabilities_mapped": len(data["capability_mappings"]),
        "parallel_authority_blocked": not assert_no_parallel_authority(),
    }, ensure_ascii=False, indent=2))
