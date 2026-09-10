import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
VISION = ROOT / "IMA_CANONICAL_VISION.md"
RUNTIME = Path(__file__).resolve().parent


def load_canonical_vision():
    if not VISION.exists():
        raise FileNotFoundError(
            f"CANONICAL VISION MISSING: {VISION}"
        )

    text = VISION.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    if not text.strip():
        raise RuntimeError("CANONICAL VISION EMPTY")

    return {
        "path": str(VISION),
        "sha256": __import__("hashlib").sha256(
            text.encode("utf-8")
        ).hexdigest(),
        "text": text,
    }


def boot_runtime():
    vision = load_canonical_vision()

    result = subprocess.check_output(
        ["node", str(RUNTIME / "IMA_RUNTIME.js")],
        text=True
    )

    runtime = json.loads(result)

    runtime["canonical_vision"] = {
        "path": vision["path"],
        "sha256": vision["sha256"],
    }

    return runtime


if __name__ == "__main__":
    print(json.dumps(
        boot_runtime(),
        ensure_ascii=False,
        indent=2
    ))
