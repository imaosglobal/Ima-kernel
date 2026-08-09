from pathlib import Path
import json
import subprocess
from datetime import datetime


BASE=Path.home()/"ima_kernel"
EVO=Path.home()/".ima/evolution"

OUT=EVO/"system_truth.json"
REGISTRY=BASE/".ima/registry/component_registry.json"


def load(path):

    if path.exists():
        try:
            return json.loads(path.read_text())
        except:
            return {}

    return {}


def save(path,data):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )
    )


def git(cmd):

    try:
        return subprocess.check_output(
            cmd,
            cwd=BASE,
            shell=True,
            text=True
        ).strip()
    except:
        return ""


def scan_files():

    result=[]

    for p in BASE.rglob("*.py"):

        try:

            result.append(
                {
                    "file":str(p.relative_to(BASE)),
                    "size":p.stat().st_size
                }
            )

        except:
            pass

    return result




def get_missing_connections():
    missing=[]

    runtime_state=Path.home()/".ima/evolution/runtime_knowledge_state.json"

    if not runtime_state.exists():
        missing.append("runtime consumption of knowledge")

    try:
        import subprocess

        import datetime

        today=datetime.date.today().isoformat()

        log=Path.home()/".ima/truth/truth_database.jsonl"

        checkpoint=False

        if log.exists():
            for line in log.read_text(encoding="utf-8").splitlines():
                if today in line and "git" in line:
                    checkpoint=True
                    break

        if not checkpoint:
            missing.append("automatic daily git checkpoint")

    except Exception:
        missing.append("automatic daily git checkpoint")

    return missing

def build():

    truth={

        "generated":
        datetime.now().isoformat(),

        "system":
        "IMA",

        "git":{

            "branch":
            git("git branch --show-current"),

            "last_commit":
            git("git log -1 --pretty=%h"),

            "last_message":
            git("git log -1 --pretty=%s")
        },


        "existing_memory":{

            "knowledge_graph":
            (BASE/"connectors/knowledge/universal_graph/knowledge_graph.json").exists(),

            "evolution_brain":
            (EVO/"evolution_brain.json").exists(),

            "daily_plan":
            (EVO/"daily_plan.json").exists(),

            "kernel_bridge":
            (EVO/"kernel_knowledge_bridge.json").exists()
        },


        "project_inventory":{

            "python_files":
            len(scan_files())

        },


        "verified_components":[],

        "missing_connections": get_missing_connections(),


        "next_actions":[

            "connect kernel runtime",

            "add guarded git sync",

            "continue minimal evolution"

        ]

    }


    registry=load(REGISTRY)

    if not registry:

        registry={

            "created":
            datetime.now().isoformat(),

            "components":[]

        }


    for name,exists in truth["existing_memory"].items():

        component={

            "name":name,

            "status":
            "verified"
            if exists
            else
            "missing",

            "checked":
            datetime.now().isoformat()

        }

        truth["verified_components"].append(
            component
        )

        registry["components"].append(
            component
        )


    save(
        OUT,
        truth
    )


    save(
        REGISTRY,
        registry
    )


    print(
        "SYSTEM TRUTH GENERATED"
    )


if __name__=="__main__":

    build()
