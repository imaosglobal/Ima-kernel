#!/data/data/com.termux/files/usr/bin/bash

BASE=$HOME/ima_kernel
mkdir -p $HOME/.ima/truth

cat > $BASE/ima_question_engine.py <<'PY'
from pathlib import Path
import json
import sys
from datetime import datetime

HOME=Path.home()
TRUTH=HOME/".ima/truth/truth_database.jsonl"
SYSTEM=HOME/".ima/evolution/system_truth.json"
EVOLUTION=HOME/".ima/evolution"


def load_json(path):
    try:
        return json.loads(path.read_text())
    except:
        return {}


def search_truth(words):
    results=[]

    if TRUTH.exists():
        for line in TRUTH.read_text().splitlines():
            try:
                item=json.loads(line)
                text=json.dumps(item,ensure_ascii=False)

                if any(w in text for w in words):
                    results.append(item)

            except:
                pass

    return results[-20:]


def answer(question):

    q=question.lower()

    words=q.split()

    print()
    print("IMA ANSWER")
    print("================")
    print("שאלה:",question)
    print()

    if any(x in q for x in ["היום","נוצר","עשינו","בוצע"]):

        print("אירועים אחרונים:")
        for e in search_truth(words+["IMA","system","evolution"]):
            print(json.dumps(e,ensure_ascii=False)[:500])
            print("---")


    elif any(x in q for x in ["חסר","בעיה","לא עובד"]):

        data=load_json(SYSTEM)

        print("חוסרים ידועים:")
        for x in data.get("missing_connections",[]):
            print("-",x)


    elif any(x in q for x in ["מצב","סטטוס","קור","מערכת"]):

        data=load_json(SYSTEM)

        print(json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        ))


    else:

        results=search_truth(words)

        if results:
            for r in results:
                print(json.dumps(
                    r,
                    ensure_ascii=False
                )[:700])
        else:
            print("אין מידע מתועד במקורות המחוברים")


if __name__=="__main__":
    answer(" ".join(sys.argv[1:]))
PY


cat > $BASE/ima <<'SH'
#!/data/data/com.termux/files/usr/bin/bash
python $HOME/ima_kernel/ima_question_engine.py "$@"
SH


chmod +x $BASE/ima

mkdir -p $HOME/bin
ln -sf $BASE/ima $HOME/bin/ima


if ! echo "$PATH" | grep -q "$HOME/bin"; then
    echo 'export PATH=$HOME/bin:$PATH' >> $HOME/.bashrc
fi


echo "IMA QUESTION ENGINE INSTALLED"
