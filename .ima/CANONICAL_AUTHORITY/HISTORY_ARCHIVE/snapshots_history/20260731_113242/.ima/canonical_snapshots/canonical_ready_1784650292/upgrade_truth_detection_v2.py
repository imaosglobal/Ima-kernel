from pathlib import Path

p=Path("system_truth_layer.py")

text=p.read_text(encoding="utf-8")

text=text.replace(
'''truth["missing_connections"] = [
    "runtime consumption of knowledge",
    "automatic daily git checkpoint"
]''',
'''missing=[]

runtime_state=Path.home()/".ima/evolution/runtime_knowledge_state.json"

if not runtime_state.exists():
    missing.append("runtime consumption of knowledge")

import subprocess

try:
    status=subprocess.check_output(
        ["git","status","--porcelain"]
    ).decode().strip()

    if status:
        missing.append("automatic daily git checkpoint")
except:
    missing.append("automatic daily git checkpoint")

truth["missing_connections"]=missing'''
)

p.write_text(text,encoding="utf-8")

print("TRUTH DETECTION V2 INSTALLED")
