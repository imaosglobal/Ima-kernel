
from pathlib import Path
import json
import hashlib
import time
import re
import os

PROJECT = Path.cwd()
ROOT = PROJECT / ".ima" / "CANONICAL_AUTHORITY"

SELF_DIR = ROOT / "evolution" / "SELF_EVOLUTION"
ENGINE_DIR = SELF_DIR / "GLOBAL_SYSTEM_AWARENESS"

SNAPSHOTS = ENGINE_DIR / "snapshots"
LOGS = ENGINE_DIR / "logs"

MANIFEST = ROOT / "CANONICAL_AUTHORITY_MANIFEST.json"
REGISTRY = ROOT / "governance" / "CANONICAL_REGISTRY.json"


EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
}


KEYWORDS = [
    "ask",
    "IMAMaster",
    "MOTHER",
    "kernel",
    "runtime",
    "memory",
    "repair",
    "evolution",
    "cognitive",
    "boot",
    "entry",
]


def sha256(path):

    h = hashlib.sha256()

    with path.open("rb") as f:

        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b""
        ):

            h.update(chunk)

    return h.hexdigest()


def safe_hash(path):

    try:

        return sha256(path)

    except Exception:

        return None


def load_json(path):

    try:

        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    except Exception:

        return {}


def canonical_paths():

    paths = {}

    if MANIFEST.is_file():

        manifest = load_json(MANIFEST)

        for key, item in manifest.get(
            "files",
            {}
        ).items():

            path = item.get(
                "canonical_path"
            )

            if path:

                paths[
                    str(
                        Path(path)
                        .resolve()
                    )
                ] = {
                    "source": "manifest",
                    "key": key,
                    "expected_sha256":
                        item.get("sha256")
                }


    if REGISTRY.is_file():

        registry = load_json(REGISTRY)

        for item in registry.get(
            "allowed_components",
            []
        ):

            path = item.get("file")

            if path:

                paths[
                    str(
                        Path(path)
                        .resolve()
                    )
                ] = {
                    "source": "registry",
                    "key": None,
                    "expected_sha256":
                        item.get("sha256")
                }

    return paths


def scan_project():

    canonical = canonical_paths()

    all_files = []

    for path in PROJECT.rglob("*"):

        if not path.is_file():

            continue

        if any(
            part in EXCLUDED_DIRS
            for part in path.parts
        ):

            continue

        all_files.append(path)


    canonical_components = []

    non_canonical = []

    conflicts = []

    keyword_hits = []

    duplicate_names = {}


    for path in all_files:

        resolved = str(
            path.resolve()
        )

        actual_hash = safe_hash(path)

        if resolved in canonical:

            info = canonical[resolved]

            item = {
                "path": str(path),
                "resolved_path": resolved,
                "classification": "CANONICAL",
                "source": info["source"],
                "key": info["key"],
                "sha256": actual_hash,
                "expected_sha256":
                    info["expected_sha256"],
                "hash_match":
                    actual_hash ==
                    info["expected_sha256"]
            }

            canonical_components.append(item)

            if not item["hash_match"]:

                conflicts.append({
                    "type":
                        "CANONICAL_HASH_MISMATCH",
                    "path": str(path),
                    "actual_sha256":
                        actual_hash,
                    "expected_sha256":
                        info["expected_sha256"]
                })

        else:

            item = {
                "path": str(path),
                "resolved_path": resolved,
                "classification":
                    "NON_CANONICAL",
                "sha256": actual_hash,
                "size": path.stat().st_size
            }

            non_canonical.append(item)


        name = path.name.lower()

        duplicate_names.setdefault(
            name,
            []
        ).append(str(path))


        if path.suffix == ".py":

            try:

                text = path.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

            except Exception:

                text = ""


            hits = [
                keyword
                for keyword in KEYWORDS
                if keyword.lower() in
                text.lower()
            ]

            if hits:

                keyword_hits.append({
                    "path": str(path),
                    "keywords": hits
                })


    for name, paths in duplicate_names.items():

        if len(paths) > 1:

            conflicts.append({
                "type":
                    "DUPLICATE_FILENAME",
                "name": name,
                "count": len(paths),
                "paths": paths[:100]
            })


    python_files = [
        item
        for item in non_canonical
        if item["path"].endswith(".py")
    ]

    json_files = [
        item
        for item in non_canonical
        if item["path"].endswith(".json")
    ]

    runtime_candidates = [
        item
        for item in keyword_hits
        if any(
            key in item["keywords"]
            for key in [
                "runtime",
                "kernel",
                "boot",
                "entry"
            ]
        )
    ]


    return {

        "component":
            "IMA_GLOBAL_SYSTEM_AWARENESS",

        "type":
            "GLOBAL_SYSTEM_AWARENESS_SNAPSHOT",

        "timestamp":
            time.time(),

        "project":
            str(PROJECT.resolve()),

        "canonical": {

            "total":
                len(canonical_components),

            "existing":
                sum(
                    1
                    for x in canonical_components
                    if Path(
                        x["path"]
                    ).is_file()
                ),

            "hash_matches":
                sum(
                    1
                    for x in canonical_components
                    if x["hash_match"]
                ),

            "hash_mismatches":
                sum(
                    1
                    for x in canonical_components
                    if not x["hash_match"]
                ),

            "components":
                canonical_components
        },

        "non_canonical": {

            "total":
                len(non_canonical),

            "python":
                len(python_files),

            "json":
                len(json_files),

            "files":
                non_canonical
        },

        "analysis": {

            "keyword_hits":
                keyword_hits,

            "runtime_candidates":
                runtime_candidates,

            "duplicate_filename_candidates":
                [
                    item
                    for item in conflicts
                    if item["type"] ==
                    "DUPLICATE_FILENAME"
                ]
        },

        "conflicts": conflicts,

        "mutation": {

            "performed": False,

            "files_modified": 0
        },

        "summary": {

            "total_files_seen":
                len(all_files),

            "canonical_files":
                len(canonical_components),

            "non_canonical_files":
                len(non_canonical),

            "conflicts":
                len(conflicts),

            "canonical_hash_mismatches":
                sum(
                    1
                    for x in canonical_components
                    if not x["hash_match"]
                ),

            "runtime_candidates":
                len(runtime_candidates),

            "keyword_hit_files":
                len(keyword_hits)
        }

    }


def main():

    SNAPSHOTS.mkdir(
        parents=True,
        exist_ok=True
    )

    LOGS.mkdir(
        parents=True,
        exist_ok=True
    )


    snapshot = scan_project()

    timestamp = int(
        time.time()
    )

    snapshot_path = (
        SNAPSHOTS
        / f"global_awareness_{timestamp}.json"
    )

    log_path = (
        LOGS
        / "global_awareness_chronological.jsonl"
    )


    snapshot_path.write_text(
        json.dumps(
            snapshot,
            ensure_ascii=False,
            indent=2
        ) + "\n",
        encoding="utf-8"
    )


    with log_path.open(
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(
                snapshot,
                ensure_ascii=False
            ) + "\n"
        )


    print("=" * 80)
    print(
        "IMA GLOBAL SYSTEM AWARENESS"
    )
    print("=" * 80)

    print()

    print(
        json.dumps(
            snapshot["summary"],
            ensure_ascii=False,
            indent=2
        )
    )

    print()

    print(
        "CANONICAL:"
    )

    print(
        json.dumps(
            snapshot["canonical"],
            ensure_ascii=False,
            indent=2
        )
    )

    print()

    print(
        "NON-CANONICAL:"
    )

    print(
        json.dumps(
            {
                key: value
                for key, value
                in snapshot["non_canonical"].items()
                if key != "files"
            },
            ensure_ascii=False,
            indent=2
        )
    )

    print()

    print(
        "CONFLICTS:",
        len(snapshot["conflicts"])
    )

    print(
        "RUNTIME CANDIDATES:",
        len(
            snapshot["analysis"]
            ["runtime_candidates"]
        )
    )

    print()

    print(
        "MUTATION PERFORMED: FALSE"
    )

    print()

    print(
        "SNAPSHOT:"
    )

    print(snapshot_path)

    print()

    print(
        "LOG:"
    )

    print(log_path)

    print("=" * 80)

    return 0


if __name__ == "__main__":

    raise SystemExit(
        main()
    )
