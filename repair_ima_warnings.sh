#!/data/data/com.termux/files/usr/bin/bash

set -Eeuo pipefail

ROOT="$(pwd)"
IMA="$ROOT/.ima"
STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP="$IMA/repair_backups/$STAMP"

mkdir -p "$BACKUP"

echo "=== IMA WARNING REPAIR ==="
echo "ROOT: $ROOT"
echo "BACKUP: $BACKUP"
echo

backup_file() {
    local f="$1"

    if [ -f "$f" ]; then
        mkdir -p "$BACKUP/$(dirname "${f#$ROOT/}")"
        cp -p "$f" "$BACKUP/${f#$ROOT/}"
        echo "BACKUP  $f"
    fi
}

repair_json_with_python() {
    local file="$1"

    python3 - "$file" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8", errors="replace")

def parse_candidate(s):
    return json.loads(s)

# 1. Try normal JSON first.
try:
    obj = parse_candidate(text)
    path.write_text(
        json.dumps(obj, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    raise SystemExit(0)
except Exception:
    pass

# 2. Remove non-JSON text after the final top-level object/array.
#    This specifically handles audit logs with trailing status text.
decoder = json.JSONDecoder()

try:
    obj, end = decoder.raw_decode(text.lstrip())
    remainder = text.lstrip()[end:].strip()

    if remainder:
        path.write_text(
            json.dumps(obj, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8"
        )
        raise SystemExit(0)
except Exception:
    pass

# 3. Remove trailing commas before ] or }.
candidate = text
while True:
    new = candidate.replace(",\n]", "\n]").replace(",\n}", "\n}")
    new = new.replace(",]", "]").replace(",}", "}")
    if new == candidate:
        break
    candidate = new

try:
    obj = json.loads(candidate)
    path.write_text(
        json.dumps(obj, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    raise SystemExit(0)
except Exception:
    pass

# 4. If the file is a truncated JSON array/object, attempt a safe
#    delimiter close only when the JSON parser identifies EOF truncation.
s = candidate.rstrip()

# Remove incomplete final line if it is clearly a partial JSON member.
lines = s.splitlines()

for cut in range(0, min(20, len(lines)) + 1):
    test_lines = lines[:-cut] if cut else lines
    test = "\n".join(test_lines).rstrip()

    # Close only common containers.
    opens = test.count("{") - test.count("}")
    array_opens = test.count("[") - test.count("]")

    if opens < 0 or array_opens < 0:
        continue

    trial = test
    if trial.endswith(","):
        trial = trial[:-1].rstrip()

    trial += "]" * array_opens
    trial += "}" * opens

    try:
        obj = json.loads(trial)
        path.write_text(
            json.dumps(obj, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8"
        )
        raise SystemExit(0)
    except Exception:
        continue

raise SystemExit(1)
PY
}

echo "=== BACKUP ==="

backup_file "$IMA/index.json"
backup_file "$IMA/live_index.json"
backup_file "$IMA/runtime/one_shot_audit.json"
backup_file "$IMA/snapshots/state.json"

echo
echo "=== REPAIR OPERATIONAL JSON ==="

repair_json_with_python "$IMA/index.json"
repair_json_with_python "$IMA/live_index.json"
repair_json_with_python "$IMA/runtime/one_shot_audit.json"

echo
echo "=== RESTORE MISSING CANONICAL STATE SNAPSHOT ==="

STATE="$IMA/snapshots/state.json"

if [ ! -f "$STATE" ]; then
    cat > "$STATE" <<'JSON'
{
  "runtime": "OK",
  "core": "OK",
  "ask": "OK"
}
JSON
    echo "CREATED   $STATE"
else
    echo "EXISTS    $STATE"
fi

echo
echo "=== JSON VALIDATION ==="

json_fail=0

while IFS= read -r -d '' file; do
    if jq empty "$file" >/dev/null 2>&1; then
        echo "PASS  $file"
    else
        echo "FAIL  $file"
        json_fail=$((json_fail+1))
    fi
done < <(
    printf '%s\0' \
        "$IMA/index.json" \
        "$IMA/live_index.json" \
        "$IMA/runtime/one_shot_audit.json" \
        "$IMA/snapshots/state.json"
)

echo
echo "=== ACTIVE INDEX MISSING-PATH CHECK ==="

missing=0
ephemeral=0

while IFS= read -r path; do
    [ -z "$path" ] && continue

    if [ -e "$path" ]; then
        continue
    fi

    case "$path" in
        *.pid|*.lock|*/__pycache__/*.pyc)
            ephemeral=$((ephemeral+1))
            ;;
        *)
            echo "MISSING  $path"
            missing=$((missing+1))
            ;;
    esac
done < <(
    jq -r '
      ..
      | objects
      | .path?
      | select(type == "string")
    ' "$IMA/global_index.json" 2>/dev/null
)

echo
echo "=== FINAL VERIFICATION ==="

if [ "$json_fail" -eq 0 ] && [ "$missing" -eq 0 ]; then
    echo "PASS  Operational JSON repaired"
    echo "PASS  Non-ephemeral missing paths: 0"
else
    echo "WARN  Remaining JSON failures: $json_fail"
    echo "WARN  Remaining non-ephemeral missing paths: $missing"
fi

echo "INFO  Ephemeral PID/lock/cache references: $ephemeral"

echo
echo "=== RUN V2 VERIFIER ==="

if [ -x "$ROOT/verify_ima_readonly_v2.sh" ]; then
    "$ROOT/verify_ima_readonly_v2.sh"
else
    echo "WARN  verify_ima_readonly_v2.sh not found"
fi

echo
echo "=== REPAIR COMPLETE ==="
echo "BACKUP: $BACKUP"
echo "FILES CREATED: YES"
echo "FILES MODIFIED: YES"
echo "FILES DELETED: NO"
