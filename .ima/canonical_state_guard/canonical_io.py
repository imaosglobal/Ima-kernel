from pathlib import Path
import json
import hashlib
import os
import subprocess
import tempfile


ROOT = Path.home() / "ima_kernel"

CANONICAL_MEMORY = (
    ROOT / "founder/data/ima_memory.json"
)

CANONICAL_JOURNAL = (
    ROOT / "founder/data/ima_learning_journal.json"
)

CANONICAL_POLICY = (
    ROOT / "founder/data/policy_memory.json"
)

CANONICAL_STARTUP = (
    ROOT / "startup/ima_memory.json"
)

STAGE = ROOT / ".ima/canonical_staging"


def _load(path, default):
    path = Path(path)

    if not path.exists():
        return default

    try:
        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )
    except Exception:
        return default


def load_memory(default=None):
    if default is None:
        default = {}

    return _load(
        CANONICAL_MEMORY,
        default
    )


def load_journal(default=None):
    if default is None:
        default = []

    return _load(
        CANONICAL_JOURNAL,
        default
    )


def load_policy(default=None):
    if default is None:
        default = {}

    return _load(
        CANONICAL_POLICY,
        default
    )


def load_startup(default=None):
    if default is None:
        default = {}

    return _load(
        CANONICAL_STARTUP,
        default
    )


def _stage(relative_name, data):
    allowed = {
        "founder/data/ima_memory.json",
        "founder/data/ima_learning_journal.json",
        "founder/data/policy_memory.json",
        "startup/ima_memory.json",
    }

    if relative_name not in allowed:
        raise PermissionError(
            "canonical target not allowed: "
            + relative_name
        )

    target = STAGE / relative_name
    target.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fd, tmp_name = tempfile.mkstemp(
        prefix=".canonical_",
        suffix=".tmp",
        dir=str(target.parent)
    )

    try:
        with os.fdopen(
            fd,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2
            )
            f.write("\n")

        os.replace(
            tmp_name,
            target
        )

    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)

    return target


def save_memory(data):
    return _stage(
        "founder/data/ima_memory.json",
        data
    )


def save_journal(data):
    return _stage(
        "founder/data/ima_learning_journal.json",
        data
    )


def save_policy(data):
    return _stage(
        "founder/data/policy_memory.json",
        data
    )


def save_startup(data):
    return _stage(
        "startup/ima_memory.json",
        data
    )


def canonical_hashes():
    result = {}

    for path in (
        CANONICAL_MEMORY,
        CANONICAL_JOURNAL,
        CANONICAL_POLICY,
        CANONICAL_STARTUP,
    ):
        if path.exists():
            result[str(path.relative_to(ROOT))] = (
                hashlib.sha256(
                    path.read_bytes()
                ).hexdigest()
            )

    return result


def promote():
    tool = ROOT / "bin/ima-canonical-promote"

    if not tool.exists():
        raise FileNotFoundError(
            "canonical promotion tool missing"
        )

    return subprocess.run(
        [str(tool)],
        cwd=ROOT,
        check=False
    ).returncode


__all__ = [
    "load_memory",
    "save_memory",
    "load_journal",
    "save_journal",
    "load_policy",
    "save_policy",
    "load_startup",
    "save_startup",
    "canonical_hashes",
    "promote",
]
