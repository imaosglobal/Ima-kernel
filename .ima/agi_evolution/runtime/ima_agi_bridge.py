#!/usr/bin/env python3
from pathlib import Path
import json
import hashlib
import time

ROOT = Path(__file__).resolve().parents[3]
EV = ROOT / ".ima" / "agi_evolution"
STATE = EV / "state" / "evolution_state.json"
PROPOSALS = EV / "proposals"

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".ima/forensic",
    ".ima/recovery",
}

TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx",
    ".json", ".md", ".txt", ".yaml", ".yml",
    ".sh", ".html", ".css"
}

MAX_ANALYSIS_SIZE = 1024 * 1024


class IMA_AGI:

    VERSION = "2.0.0"

    @classmethod
    def load_state(cls):
        if STATE.exists():
            try:
                data = json.loads(
                    STATE.read_text(encoding="utf-8")
                )
                if isinstance(data, dict):
                    return data
            except Exception:
                pass

        return {
            "version": cls.VERSION,
            "runs": 0,
            "files_seen": 0,
            "knowledge_candidates": 0,
            "large_files": 0,
            "proposals_created": 0,
        }

    @classmethod
    def save_state(cls, state):
        STATE.parent.mkdir(parents=True, exist_ok=True)

        tmp = STATE.with_suffix(".tmp")
        tmp.write_text(
            json.dumps(
                state,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )
        tmp.replace(STATE)

    @classmethod
    def inventory(cls):

        files = []
        candidates = []
        large = []

        for p in ROOT.rglob("*"):

            if not p.is_file():
                continue

            try:
                rel = str(
                    p.relative_to(ROOT)
                ).replace("\\", "/")
            except ValueError:
                continue

            if any(
                rel == d or rel.startswith(d + "/")
                for d in IGNORE_DIRS
            ):
                continue

            try:
                size = p.stat().st_size
            except OSError:
                continue

            item = {
                "path": rel,
                "size": size,
            }

            files.append(item)

            if size > MAX_ANALYSIS_SIZE:
                large.append(item)

            elif p.suffix.lower() in TEXT_EXTENSIONS:
                candidates.append(item)

        return {
            "files": len(files),
            "knowledge_candidates": len(candidates),
            "large_files": len(large),
            "largest": sorted(
                files,
                key=lambda x: x["size"],
                reverse=True
            )[:30],
        }

    @classmethod
    def create_proposal(cls, message, context, inventory):

        ident = hashlib.sha256(
            f"{time.time_ns()}:{message}".encode()
        ).hexdigest()[:16]

        proposal = {
            "id": f"evolution_{ident}",
            "time": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ",
                time.gmtime()
            ),
            "creator": "Ori Cohen",
            "version": cls.VERSION,
            "trigger": message,
            "context": context,
            "inventory": inventory,

            "learning_policy": {
                "archive_is_knowledge": True,
                "runtime_loads_archive_wholesale": False,
                "inspect_before_promotion": True,
                "preserve_provenance": True,
                "preserve_history": True,
            },

            "evolution_pipeline": [
                "inspect",
                "classify",
                "deduplicate",
                "identify_valuable_knowledge",
                "identify_redundant_material",
                "propose_compression",
                "propose_code_improvement",
                "test",
                "validate",
                "promote_only_if_valid",
            ],

            "automatic_deletion": False,
            "status": "PROPOSED",
        }

        path = PROPOSALS / f"{proposal['id']}.json"

        path.write_text(
            json.dumps(
                proposal,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        return str(path.relative_to(ROOT))

    @classmethod
    def process(cls, message, context=None):

        context = context or {}

        state = cls.load_state()
        state["runs"] += 1

        inv = cls.inventory()

        state["files_seen"] = inv["files"]
        state["knowledge_candidates"] = (
            inv["knowledge_candidates"]
        )
        state["large_files"] = inv["large_files"]

        proposal = cls.create_proposal(
            message,
            context,
            inv
        )

        state["proposals_created"] += 1

        cls.save_state(state)

        return {
            "status": "ACTIVE",
            "version": cls.VERSION,
            "mode": "SELF_INSPECTION_AND_EVOLUTION",
            "archive_learning": True,
            "weight_aware": True,
            "self_improvement_pipeline": True,
            "provenance": True,
            "automatic_deletion": False,
            "inventory": inv,
            "proposal": proposal,
        }
