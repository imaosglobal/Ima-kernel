#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "INSTALLING IMA SYSTEM TRUTH LAYER"

mkdir -p ~/.ima/evolution
mkdir -p .ima/registry


cat > system_truth_layer.py <<'PY'
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

        "missing_connections":[

            "runtime consumption of knowledge",

            "automatic daily git checkpoint"

        ],


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
PY


python system_truth_layer.py


cat > connect_system_truth_daily.py <<'PY'
from pathlib import Path

p=Path("daily_evolution.py")

if p.exists():

    text=p.read_text()

    marker='''IMA DAILY EVOLUTION SAVED'''

    if "system_truth_layer.py" not in text:

        text=text.replace(
            marker,
            marker+'''

    import os
    os.system(
        "python system_truth_layer.py"
    )'''
        )

        p.write_text(text)

print("SYSTEM TRUTH CONNECTED TO DAILY EVOLUTION")
PY


python connect_system_truth_daily.py

python system_truth_layer.py


echo "SYSTEM TRUTH LAYER INSTALLED"
