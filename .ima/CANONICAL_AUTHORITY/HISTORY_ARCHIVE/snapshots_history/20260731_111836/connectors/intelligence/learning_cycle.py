import subprocess
from pathlib import Path
from datetime import datetime
import json

BASE = Path(__file__).parent.parent


def run(step):
    print("[RUN]", step)
    subprocess.run(step, shell=True)


def report():

    files=[
        "knowledge/software_memory.jsonl",
        "knowledge/concepts_memory.json",
        "knowledge/capability_graph.json"
    ]

    result={
        "time":datetime.now().isoformat(),
        "memory":{}
    }

    for f in files:
        p=BASE/f
        if p.exists():
            result["memory"][f]=p.stat().st_size

    Path(
        BASE/"knowledge/learning_report.json"
    ).write_text(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )


if __name__=="__main__":

    run(
        "python scanner/scanner_agent.py"
    )

    run(
        "python intelligence/knowledge_engine.py"
    )

    run(
        "python intelligence/consolidator.py"
    )

    run(
        "python intelligence/pattern_engine.py"
    )

    run(
        "python intelligence/principle_engine.py"
    )

    run(
        "python intelligence/memory_resolution_engine.py"
    )

    run(
        "python intelligence/compression_engine.py"
    )

    run(
        "python intelligence/self_expansion_engine.py"
    )

    run(
        "python intelligence/relation_learning_engine.py"
    )

    report()

    
import shutil

shutil.copy(
    BASE/"knowledge/concepts_memory.json",
    Path.home()/".ima/memory/software_concepts.json"
)


import shutil

# Universal Knowledge Bridge
src = BASE/"knowledge/universal_graph/knowledge_graph.json"
dst = Path.home()/".ima/memory/universal_knowledge_graph.json"

if src.exists():
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, dst)

print("IMA LEARNING CYCLE COMPLETE")
