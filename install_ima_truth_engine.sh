#!/data/data/com.termux/files/usr/bin/bash
set -e

BASE="$HOME/ima_kernel"
TRUTH="$HOME/.ima/truth"

mkdir -p "$TRUTH"

cat > "$BASE/truth_engine.py" <<'PY'
import json
import subprocess
from pathlib import Path
from datetime import datetime

BASE=Path.home()/"ima_kernel"
OUT=Path.home()/".ima/truth/truth_database.jsonl"
CURRENT=Path.home()/".ima/truth/current_truth.json"

SOURCES=[
    Path.home()/".ima/evolution/system_truth.json",
    Path.home()/".ima/evolution/evolution_brain.json",
    Path.home()/".ima/evolution/daily_plan.json",
    Path.home()/".ima/evolution/next_session.json",
    BASE/".ima/daily/current_state.json",
    BASE/".ima/evolution/evolution_map.json",
    BASE/".ima/evolution/system_capabilities.json"
]


def git_history():
    try:
        r=subprocess.check_output(
            ["git","log","--pretty=format:%h|%ad|%s","--date=short"],
            cwd=BASE,
            text=True
        )
        return r.splitlines()
    except:
        return []


def scan():

    events=[]

    for src in SOURCES:
        if src.exists():
            try:
                data=json.loads(src.read_text())
                events.append({
                    "time":datetime.now().isoformat(),
                    "source":str(src),
                    "data":data
                })
            except:
                pass


    for item in git_history():
        parts=item.split("|",2)
        if len(parts)==3:
            events.append({
                "time":parts[1],
                "source":"git",
                "commit":parts[0],
                "event":parts[2]
            })


    with OUT.open("w",encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e,ensure_ascii=False)+"\n")


    truth={
        "updated":datetime.now().isoformat(),
        "events":len(events),
        "sources_scanned":len(SOURCES),
        "git_events":len(git_history()),
        "database":str(OUT)
    }

    CURRENT.write_text(
        json.dumps(truth,indent=2,ensure_ascii=False)
    )



if __name__=="__main__":
    scan()
PY


cat > "$BASE/truth_query.py" <<'PY'
import json,sys
from pathlib import Path

DB=Path.home()/".ima/truth/truth_database.jsonl"

query=" ".join(sys.argv[1:]).lower()

found=[]

if DB.exists():
    for line in DB.read_text().splitlines():
        try:
            obj=json.loads(line)
            text=json.dumps(obj,ensure_ascii=False).lower()
            if any(x in text for x in query.split()):
                found.append(obj)
        except:
            pass



if not found:
else:
    for item in found[-10:]:
PY


cat > "$BASE/ima-truth" <<'SH'
#!/data/data/com.termux/files/usr/bin/bash
python $HOME/ima_kernel/truth_engine.py >/dev/null
python $HOME/ima_kernel/truth_query.py "$@"
SH


chmod +x "$BASE/ima-truth"

mkdir -p "$HOME/bin"

ln -sf "$BASE/ima-truth" "$HOME/bin/ima-truth"

if ! echo "$PATH" | grep -q "$HOME/bin"; then
    echo 'export PATH=$HOME/bin:$PATH' >> "$HOME/.bashrc"
fi


python "$BASE/truth_engine.py"

echo "IMA TRUTH ENGINE INSTALLED"
