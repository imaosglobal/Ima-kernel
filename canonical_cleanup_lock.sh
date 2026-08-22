#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

echo "=== IMA CANONICAL CLEANUP + LOCK ==="

STAMP=$(date +%Y%m%d_%H%M%S)
BACKUP=".ima/backups/canonical_cleanup_$STAMP"

mkdir -p "$BACKUP"

echo "[1] Backup"

for f in \
kernel/release.js \
kernel/releases/v1778001671191/ima_self_heal.js \
kernel/releases/v1778001671191/server.js
do
    if [ -f "$f" ]; then
        mkdir -p "$BACKUP/$(dirname "$f")"
        cp "$f" "$BACKUP/$f"
    fi
done

echo "[2] Remove stale runtime references from active release files"

if [ -f kernel/release.js ]; then
python3 - <<'PY'
from pathlib import Path

p=Path("kernel/release.js")

s=p.read_text()

s=s.replace(
'"ima_kernel.js","ima_runtime.js","ima_policy.js","ima_memory_long.js"',
'"runtime/ENTRYPOINT.js"'
)

p.write_text(s)
PY
fi


echo "[3] Replace old self heal in release snapshot"

if [ -f kernel/releases/v1778001671191/ima_self_heal.js ]; then

cat > kernel/releases/v1778001671191/ima_self_heal.js <<'JS'
const fs = require('fs');

function heal(){

const required=[
'.ima/runtime/runtime.py',
'learning/meta_orchestrator.py',
'.ima/governance/canonical_architecture.json'
];

required.forEach(f=>{
 if(fs.existsSync(f)){
  console.log('[HEAL OK]',f);
 }else{
  console.log('[HEAL MISSING]',f);
 }
});

console.log('[CANONICAL RELEASE HEAL CHECK]');
}

module.exports={heal};
JS

fi


echo "[4] Verify active requires"

grep -RIn \
"require.*ima_runtime\|require.*ima_policy\|require.*ima_kernel" \
kernel learning .ima \
--exclude-dir=.git \
--exclude-dir=_graveyard \
--exclude-dir=__pycache__ \
|| true


echo "[5] Canonical verification"

python3 - <<'PY'
from pathlib import Path
import json

checks=[
Path(".ima/runtime/runtime.py"),
Path("learning/meta_orchestrator.py"),
Path(".ima/governance/canonical_architecture.json")
]

ok=True

for c in checks:
    if c.exists():
    else:
        ok=False

if not ok:
    raise SystemExit(1)

PY


echo "[6] Create lock"

cat > .ima/governance/CANONICAL_LOCK_FINAL.json <<JSON
{
 "state":"CANONICAL_LOCKED",
 "runtime":".ima/runtime/runtime.py",
 "brain":"learning/meta_orchestrator.py",
 "architecture":".ima/governance/canonical_architecture.json",
 "legacy_node_runtime":"kernel/_legacy_node_runtime",
 "timestamp":"$(date -Iseconds)"
}
JSON


echo "[7] Final scan"

find kernel -maxdepth 2 -type f \
| grep -E "ima_runtime.js|ima_policy.js|ima_kernel.js" \
|| true


echo "=== IMA CANONICAL LOCK COMPLETE ==="
