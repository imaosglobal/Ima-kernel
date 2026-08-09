import json
from pathlib import Path

p=Path(".ima/agi_evolution/CAPABILITY_REGISTRY.json")

def run():
    data=json.loads(p.read_text())

    report={}

    for k,v in data["capabilities"].items():
        report[k]=v.get("status","unknown")

    Path(".ima/agi_evolution/runtime/AGI_STATUS.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False)
    )

    return report


if __name__=="__main__":
    print(run())
