#!/data/data/com.termux/files/usr/bin/bash
set -e

BASE="$HOME/ima_kernel"
TRUTH="$HOME/.ima/truth"

mkdir -p "$TRUTH"

cat > "$BASE/truth_engine.py" <<'PY'
import json
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime,date

BASE=Path.home()/"ima_kernel"
TRUTH=Path.home()/".ima/truth"

DB=TRUTH/"truth_database.jsonl"
SUMMARY=TRUTH/"current_truth.json"


SOURCES=[
    Path.home()/".ima/evolution/system_truth.json",
    Path.home()/".ima/evolution/evolution_brain.json",
    Path.home()/".ima/evolution/daily_plan.json",
    Path.home()/".ima/evolution/next_session.json",
    BASE/".ima/daily/current_state.json"
]


def normalize(text):
    return " ".join(
        str(text).lower().split()
    )


    return hashlib.sha256(
        normalize(text).encode()
    ).hexdigest()


def git_events():

    result=[]

    try:
        out=subprocess.check_output(
            [
                "git",
                "log",
                "--pretty=format:%h|%ad|%s",
                "--date=short"
            ],
            cwd=BASE,
            text=True
        )

        seen=set()

        for line in out.splitlines():

            p=line.split("|",2)

            if len(p)!=3:
                continue

                p[1]+p[2]
            )

            if key in seen:
                continue

            seen.add(key)

            result.append({
                "date":p[1],
                "source":"git",
                "commit":p[0],
                "event":p[2]
            })

    except:
        pass

    return result


def load_json_sources():

    result=[]

    for src in SOURCES:

        if src.exists():

            try:
                data=json.loads(
                    src.read_text()
                )

                result.append({
                    "date":datetime.now().strftime("%Y-%m-%d"),
                    "source":str(src),
                    "data":data
                })

            except:
                pass

    return result


def build():

    events=[]

    events.extend(
        load_json_sources()
    )

    events.extend(
        git_events()
    )


    with DB.open(
        "w",
        encoding="utf-8"
    ) as f:

        for e in events:
            f.write(
                json.dumps(
                    e,
                    ensure_ascii=False
                )
                + "\n"
            )


    today=str(date.today())

    summary={
        "updated":datetime.now().isoformat(),
        "today":today,
        "total_events":len(events),
        "sources":[
            "git",
            "system_truth",
            "evolution",
            "daily_state"
        ],
        "status":"verified",
        "database":str(DB)
    }


    SUMMARY.write_text(
        json.dumps(
            summary,
            indent=2,
            ensure_ascii=False
        )
    )




if __name__=="__main__":
    build()
PY


cat > "$BASE/truth_query.py" <<'PY'
import json
import sys
from pathlib import Path
from datetime import date,timedelta

DB=Path.home()/".ima/truth/truth_database.jsonl"

q=" ".join(sys.argv[1:]).lower()

today=str(date.today())

if "היום" in q or "today" in q:
    q=q.replace("היום","").strip()


events=[]

if DB.exists():

    for line in DB.read_text().splitlines():

        try:
            events.append(
                json.loads(line)
            )
        except:
            pass


matches=[]

for e in events:

    text=json.dumps(
        e,
        ensure_ascii=False
    ).lower()

    if not q:
        matches.append(e)

    elif any(
        word in text
        for word in q.split()
    ):
        matches.append(e)



if not matches:
else:

        "נמצאו",
        len(matches),
        "אירועים"
    )

    for e in matches[-15:]:

        if "event" in e:
                f"[{e.get('date',e.get('time'))}] {e['event']}"
            )

        else:
                json.dumps(
                    e,
                    ensure_ascii=False
                )[:500]
            )
PY


python "$BASE/truth_engine.py"

echo "IMA TRUTH ENGINE V2 INSTALLED"
