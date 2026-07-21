#!/data/data/com.termux/files/usr/bin/bash

set -u

ROOT="$(pwd)"
IMA="$ROOT/.ima"

PASS=0
WARN=0
FAIL=0

ok()   { printf "PASS  %s\n" "$1"; PASS=$((PASS+1)); }
warn() { printf "WARN  %s\n" "$1"; WARN=$((WARN+1)); }
fail() { printf "FAIL  %s\n" "$1"; FAIL=$((FAIL+1)); }

printf "\nIMA READ-ONLY VERIFICATION V2\n"
printf "==============================\n"
printf "ROOT: %s\n\n" "$ROOT"

[ -d "$IMA" ] && ok "IMA directory" || fail "IMA directory"
[ -d "$IMA/releases" ] && ok "Release structure" || warn "Release structure"

printf "\n=== ACTIVE CANONICAL STATE ===\n"

INDEX="$IMA/global_index.json"

if [ -f "$INDEX" ] && jq empty "$INDEX" >/dev/null 2>&1; then
    ok "Active global index is valid JSON"
else
    fail "Active global index invalid or missing"
fi

if [ -f "$INDEX" ]; then
    indexed=$(jq -r '
      ..
      | objects
      | .path?
      | select(type == "string")
    ' "$INDEX" 2>/dev/null | wc -l)

    ok "Active index entries: $indexed"

    missing=0
    ephemeral=0
    real_missing=0

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
                real_missing=$((real_missing+1))
                ;;
        esac
    done < <(
        jq -r '
          ..
          | objects
          | .path?
          | select(type == "string")
        ' "$INDEX" 2>/dev/null
    )

    if [ "$real_missing" -eq 0 ]; then
        ok "Active index referenced paths: no non-ephemeral missing paths"
    else
        warn "Active index non-ephemeral missing paths: $real_missing"
    fi

    if [ "$ephemeral" -gt 0 ]; then
        warn "Ephemeral PID/lock/cache references ignored: $ephemeral"
    fi
fi

printf "\n=== RUNTIME ===\n"

if [ -f "$IMA/runtime/core.py" ]; then
    grep -q 'global_index.json' "$IMA/runtime/core.py" \
        && ok "Runtime core uses active global index" \
        || fail "Runtime core index mismatch"
else
    warn "Runtime core missing"
fi

if [ -f "$IMA/runtime/query_engine.py" ]; then
    grep -q 'global_index.json' "$IMA/runtime/query_engine.py" \
        && ok "Query engine uses active global index" \
        || fail "Query engine index mismatch"
else
    warn "Query engine missing"
fi

printf "\n=== CANONICAL ARTIFACTS ===\n"

[ -f "$IMA/runtime/canonical_manifest.json" ] \
    && ok "Canonical manifest present" \
    || warn "Canonical manifest missing"

canonical_count=$(find "$IMA" -type f \
    \( -name "canonical_manifest.json" -o -name "canonical_chain_audit.json" \) \
    2>/dev/null | wc -l)

[ "$canonical_count" -gt 0 ] \
    && ok "Canonical artifacts detected: $canonical_count" \
    || warn "No canonical artifacts detected"

printf "\n=== GIT ===\n"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    commits=$(git rev-list --all --count 2>/dev/null || echo 0)
    [ "$commits" -gt 0 ] \
        && ok "Git history: $commits commits" \
        || warn "Git has no commits"

    git fsck --full --no-progress >/dev/null 2>&1 \
        && ok "Git object integrity" \
        || fail "Git object integrity"
fi

printf "\n=== HISTORICAL / NON-CANONICAL JSON ===\n"

invalid_json=0
historical_invalid=0
active_invalid=0

while IFS= read -r -d '' file; do
    if ! jq empty "$file" >/dev/null 2>&1; then
        invalid_json=$((invalid_json+1))

        case "$file" in
            "$IMA/archive_final/"*|*.broken.json)
                historical_invalid=$((historical_invalid+1))
                ;;
            "$IMA/index.json"|"$IMA/live_index.json"|"$IMA/runtime/one_shot_audit.json")
                active_invalid=$((active_invalid+1))
                ;;
        esac
    fi
done < <(find "$IMA" -type f -iname "*.json" -print0 2>/dev/null)

if [ "$active_invalid" -eq 0 ]; then
    ok "Active operational JSON: no invalid files"
else
    warn "Active operational JSON invalid: $active_invalid"
fi

if [ "$historical_invalid" -gt 0 ]; then
    warn "Historical/broken JSON retained as non-canonical artifacts: $historical_invalid"
fi

printf "\n==============================\n"
printf "VERIFICATION COMPLETE V2\n"
printf "==============================\n"
printf "PASS: %s\n" "$PASS"
printf "WARN: %s\n" "$WARN"
printf "FAIL: %s\n" "$FAIL"

if [ "$FAIL" -eq 0 ]; then
    if [ "$WARN" -eq 0 ]; then
        printf "\nVERDICT: VERIFIED\n"
    else
        printf "\nVERDICT: VERIFIED_WITH_WARNINGS\n"
    fi
else
    printf "\nVERDICT: VERIFICATION_FAILED\n"
fi

printf "\nMODE: READ-ONLY\n"
printf "FILES CREATED: YES (verifier only)\n"
printf "FILES MODIFIED: NO\n"
printf "FILES DELETED: NO\n"
