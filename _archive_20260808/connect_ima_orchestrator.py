from pathlib import Path
import json
import time
import shutil

ROOT = Path(".")
stamp = str(int(time.time()))


# backup
backup = ROOT / f".ima/orchestrator_backup_{stamp}"
backup.mkdir(parents=True, exist_ok=True)

for f in [
    "ima_fusion_runtime.py",
    "ima_self_knowledge_bridge.py"
]:
    p = ROOT / f
    if p.exists():
        shutil.copy2(p, backup / f)


# update fusion runtime
fusion = ROOT / "ima_fusion_runtime.py"

if fusion.exists():
    text = fusion.read_text(encoding="utf-8")

    if 'meta_orchestrator' not in text:
        text = text.replace(
            '"learning": safe_import("learning.meta_orchestrator")',
            '"learning": safe_import("learning.meta_orchestrator"),\n    "orchestrator": safe_import("learning.meta_orchestrator")'
        )

    if 'meta_learning' not in text:
        text = text.replace(
            'return router["module"].ask(message)',
            '''
            response = router["module"].ask(message)

            try:
                meta = LAYERS["orchestrator"]
                if meta.get("connected"):
                    response["meta_learning"] = meta["module"].run_meta_analysis()
            except Exception as e:
                response["meta_learning_error"] = str(e)

            return response
            '''
        )

    fusion.write_text(text, encoding="utf-8")

# update self knowledge registry
registry = ROOT / ".ima/ima_self_knowledge_registry.json"

data = {}

if registry.exists():
    try:
        data = json.loads(registry.read_text(encoding="utf-8"))
    except:
        data = {}

data["runtime_architecture"] = {
    "fusion_runtime": "ima_fusion_runtime.py",
    "master_runtime": "ima_master_runtime.py",
    "core_runtime": "ima_core_runtime.py",
    "brain": "ima_brain.py",
    "orchestrator": "learning/meta_orchestrator.py",
    "mother_layer": "ima_mom.py"
}

data["governance"] = {
    "single_orchestrator": True,
    "canonical_orchestrator": "learning/meta_orchestrator.py",
    "prevent_duplicates": True
}

registry.parent.mkdir(exist_ok=True)

registry.write_text(
    json.dumps(
        data,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)


# verification

checks = [
    "ima_fusion_runtime.py",
    "learning/meta_orchestrator.py",
    ".ima/ima_self_knowledge_registry.json"
]

for c in checks:
        c,
        "OK" if (ROOT / c).exists() else "MISSING"
    )

