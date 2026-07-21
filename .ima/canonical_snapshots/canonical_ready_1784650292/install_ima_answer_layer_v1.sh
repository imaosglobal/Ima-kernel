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

    print("IMA")
    print("================")
    print("שאלה:",question)
    print()

    if "היום" in question or "עשינו" in question:

        print("סיכום היום:")

        print("בוצעו בדיקות וחיבורים למערכת:")

        for c in truth.get("verified_components",[]):
            print("✅",c["name"])

        print()

        if brain:
            for x in brain.get("current_state",{}).get("domains",[]):
                print("תחום:",x)

        print()

        missing=truth.get("missing_connections",[])
        if missing:
            print("עדיין חסר:")
            for m in missing:
                print("⚠️",m)

    elif "חסר" in question:
        print("חוסרים ידועים:")
        for x in truth.get("missing_connections",[]):
            print("-",x)

    elif "הבא" in question or "המשך" in question:
        print("הצעדים הבאים:")
        for x in plan.get("goals",[]):
            print("-",x.get("goal"))

    else:
        print("נמצאו נתוני מערכת:")
        print(json.dumps(truth,ensure_ascii=False,indent=2))


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
