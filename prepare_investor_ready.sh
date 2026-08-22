#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMA INVESTOR READINESS SCAN ==="

mkdir -p docs
mkdir -p investor
mkdir -p demo

echo "[1] SYSTEM INVENTORY"

python3 - <<'PY'
from pathlib import Path
import json

root=Path(".")
data={
    "python_files":len(list(root.rglob("*.py"))),
    "json_files":len(list(root.rglob("*.json"))),
    "markdown_files":len(list(root.rglob("*.md"))),
    "git_exists":(root/".git").exists()
}

Path("docs/system_inventory.json").write_text(
    json.dumps(data,indent=2,ensure_ascii=False)
)

PY


echo "[2] CREATE PRODUCT DOCUMENTS"

cat > docs/vision.md <<'EOF'
# IMA Vision

IMA is a personal AI memory and learning platform.

Core principles:
- Long term memory
- Controlled learning
- Pattern extraction
- Human centered AI
EOF


cat > docs/architecture.md <<'EOF'
# IMA Architecture

Layers:

Runtime
 |
 Brain
 |
 Memory
 |
 Learning Loop
 |
 Learning Gate
 |
 Pattern Extraction
 |
 Historical Inference
EOF


cat > investor/one_pager.md <<'EOF'
# IMA One Pager

## Problem
Current AI assistants forget context and lack continuous personal understanding.

## Solution
IMA creates a personal intelligence layer with memory, learning and insight extraction.

## Current Technology
- AI runtime
- Persistent memory
- Learning pipeline
- Pattern detection
- Historical inference
- Self improvement planning

## Next Stage
Productization, team building and partnerships.
EOF


cat > investor/pitch_outline.md <<'EOF'
# IMA Pitch

1. Vision
2. Problem
3. Solution
4. Technology
5. Demo
6. Market
7. Business model
8. Roadmap
9. Team
10. Investment
EOF


cat > demo/demo_flow.md <<'EOF'
# Demo Flow

User speaks.

↓

IMA stores memory.

↓

Learning system detects patterns.

↓

IMA produces insights.

↓

IMA improves interaction.
EOF


echo "[3] CREATE STATUS REPORT"

python3 - <<'PY'
from pathlib import Path
import subprocess

status=subprocess.getoutput("git status --short")

Path("docs/git_status_report.txt").write_text(status)

PY


echo "[4] VERIFY CORE IMPORTS"

python3 - <<'PY'
mods=[
"ima_brain",
"ima_master_runtime",
"learning.learning_loop",
"learning.meta_orchestrator",
"learning.historical_inference"
]

for m in mods:
    try:
        __import__(m)
    except Exception as e:
PY


echo "=== COMPLETE ==="
