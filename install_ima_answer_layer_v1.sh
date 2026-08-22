#!/data/data/com.termux/files/usr/bin/bash

BASE=$HOME/ima_kernel

cat > $BASE/answer_builder.py <<'PY'
import json
from pathlib import Path
from datetime import datetime

HOME=Path.home()

def load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except:
        return {}

def build_answer(question):

    truth=load(HOME/".ima/evolution/system_truth.json")
    brain=load(HOME/".ima/evolution/evolution_brain.json")
    plan=load(HOME/".ima/evolution/daily_plan.json")
    bridge=load(HOME/".ima/evolution/kernel_knowledge_bridge.json")


    if "היום" in question or "עשינו" in question:



        for c in truth.get("verified_components",[]):


        if brain:
            for x in brain.get("current_state",{}).get("domains",[]):


        missing=truth.get("missing_connections",[])
        if missing:
            for m in missing:

    elif "חסר" in question:
        for x in truth.get("missing_connections",[]):

    elif "הבא" in question or "המשך" in question:
        for x in plan.get("goals",[]):

    else:


if __name__=="__main__":
    import sys
    build_answer(" ".join(sys.argv[1:]))
PY


cat > $BASE/ima_answer <<'SH'
#!/data/data/com.termux/files/usr/bin/bash
python $HOME/ima_kernel/answer_builder.py "$@"
SH

chmod +x $BASE/ima_answer

mkdir -p $HOME/bin
ln -sf $BASE/ima_answer $HOME/bin/ima-answer

echo "IMA ANSWER LAYER INSTALLED"
