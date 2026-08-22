from pathlib import Path
import json
import datetime
import importlib.util


ROOT = Path(".")
IMA = Path(".ima")

OUTPUT = IMA / "ima_self_knowledge_registry.json"


SEARCH_MODULES = [
    "learning.learning_memory",
    "learning.self_reflection",
    "learning.meta_orchestrator",
    "learning.ima_awareness",
    "learning.health_check",
    "ima_system",
    "ima_master_runtime",
    "ima_core_runtime",
]


REPORT_FILES = [
    ".ima/ima_sync_tree.json",
    ".ima/ima_dependency_map.json",
    ".ima/ima_runtime_map.json",
    ".ima/ima_architecture_report.json",
    ".ima/ima_control_flow.json",
]


def check_module(name):
    try:
        spec = importlib.util.find_spec(name)
        return {
            "module": name,
            "exists": spec is not None,
            "location": str(spec.origin) if spec else None
        }
    except Exception as e:
        return {
            "module": name,
            "exists": False,
            "error": str(e)
        }


def load_reports():

    reports = {}

    for file in REPORT_FILES:

        path = Path(file)

        if path.exists():

            try:
                reports[file] = json.loads(
                    path.read_text(
                        encoding="utf-8"
                    )
                )

            except Exception as e:

                reports[file] = {
                    "error": str(e)
                }

    return reports



def collect_capabilities():

    capabilities = {}

    folders = [
        "founder",
        "languages",
        "learning",
        "product",
        "ima-ui"
    ]

    for folder in folders:

        path = Path(folder)

        capabilities[folder] = {
            "exists": path.exists(),
            "files": len(
                list(path.rglob("*"))
            ) if path.exists() else 0
        }

    return capabilities



def build_registry():

    registry = {

        "identity": "IMA",

        "type": "self_knowledge_layer",

        "created":
            str(datetime.datetime.now()),


        "existing_intelligence": {

            "modules": [
                check_module(x)
                for x in SEARCH_MODULES
            ]

        },


        "architecture":

            load_reports(),


        "capabilities":

            collect_capabilities(),


        "learning_instruction": {

            "purpose":
            "IMA learns from system state",

            "future_updates":
            [
                "detect_missing_capabilities",
                "detect_duplicate_modules",
                "recommend_improvements",
                "validate_changes"
            ]

        }

    }


    return registry



IMA.mkdir(
    exist_ok=True
)


registry = build_registry()


OUTPUT.write_text(
    json.dumps(
        registry,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)



for module in registry["existing_intelligence"]["modules"]:
        module["module"],
        "OK" if module["exists"] else "MISSING"
    )



