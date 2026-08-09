
from pathlib import Path
import json,time

SCOPE=Path(".ima/global_self_improvement_scope.json")
REPORT=Path(".ima/self_improvement_report.json")

def load_scope():
    return json.loads(SCOPE.read_text(encoding="utf-8"))

def scan():
    scope=load_scope()
    report={
        "time":time.time(),
        "components":[],
        "missing":[],
        "existing":[]
    }

    for target in scope.get("targets",[]):
        component={
            "name":target["name"],
            "paths":[]
        }

        for p in target.get("paths",[]):
            path=Path(p)

            if path.exists():
                report["existing"].append(str(path))
                component["paths"].append({
                    "path":str(path),
                    "status":"exists"
                })
            else:
                report["missing"].append(str(path))
                component["paths"].append({
                    "path":str(path),
                    "status":"missing"
                })

        report["components"].append(component)

    REPORT.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    return report

if __name__=="__main__":
    print(json.dumps(scan(),ensure_ascii=False,indent=2))
