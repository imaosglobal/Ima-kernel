from pathlib import Path
import json
import shutil
import time


backup=Path(
    f"learning_backup_adaptive_{int(time.time())}"
)

shutil.copytree(
    "learning",
    backup
)



# policy

policy={
    "max_background_sources_per_cycle":3,
    "max_memory_mb":200,
    "keep_raw_html":False,
    "compression":True,
    "duplicate_threshold":0.92,
    "trust_required":60,
    "sleep_between_cycles":3600
}

Path(
"learning/learning_policy.json"
).write_text(
    json.dumps(policy,indent=2),
    encoding="utf8"
)


# source ranker

Path(
"learning/source_quality_ranker.py"
).write_text(
'''
WEIGHTS={
"Nature":1.0,
"PubMed":1.0,
"NASA":0.95,
"NOAA":0.95,
"MIT":0.95,
"arXiv":0.9,
"Google Scholar":0.85,
"Wikipedia":0.7,
"DuckDuckGo":0.5
}

def rank(source,trust=0):

    base=WEIGHTS.get(
        source,
        0.4
    )

    return round(
        base*(trust/100 if trust else 1),
        3
    )
''',
encoding="utf8"
)


# compactor

Path(
"learning/knowledge_compactor.py"
).write_text(
'''
import hashlib


    return hashlib.sha256(
        text.encode("utf8")
    ).hexdigest()


def compact(text):

    if not text:
        return ""

    text=" ".join(
        text.split()
    )

    return text[:3000]
''',
encoding="utf8"
)


# adaptive daemon

Path(
"learning/adaptive_learning_daemon.py"
).write_text(
'''
import time
import json
from pathlib import Path

POLICY=json.loads(
Path(
"learning/learning_policy.json"
).read_text()
)


def learning_cycle():

    "[ADAPTIVE LEARNING]"
    )

    "Resource limit:",
    POLICY["max_memory_mb"],
    "MB"
    )

    "Sources per cycle:",
    POLICY["max_background_sources_per_cycle"]
    )

    # future source discovery hook
    # never loads unlimited data

    return True


if __name__=="__main__":

    while True:

        learning_cycle()

        time.sleep(
            POLICY["sleep_between_cycles"]
        )
'''
,
encoding="utf8"
)




# compile

import subprocess

failed=[]

for p in Path("learning").rglob("*.py"):

    r=subprocess.run(
        [
        "python3",
        "-m",
        "py_compile",
        str(p)
        ],
        capture_output=True
    )

    if r.returncode:
        failed.append(str(p))


if failed:
    for f in failed:
else:


