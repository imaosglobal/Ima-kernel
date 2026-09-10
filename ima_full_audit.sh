#!/data/data/com.termux/files/usr/bin/bash
set -u

ROOT="$PWD"
STAMP="$(date +%Y%m%d_%H%M%S)"
REPORT="$ROOT/IMA_AUDIT_$STAMP.md"
BACKUP="$ROOT/.ima/audit_backup_$STAMP.patch"

mkdir -p "$ROOT/.ima"

exec > >(tee "$REPORT") 2>&1

echo "# IMA Full Audit — $STAMP"
echo
echo "## 1. Repository"
git rev-parse --show-toplevel
git branch --show-current
git status --short
echo

echo "## 2. HEAD"
git log -1 --oneline
echo

echo "## 3. Existing work is protected"
git diff --binary > "$BACKUP" || true
git diff --stat || true
git status --short
echo "Backup patch: $BACKUP"
echo

echo "## 4. Python syntax"
python -m compileall -q . \
  -x '(^|/)(\.git|node_modules|venv|\.venv|dist|build|__pycache__)(/|$)' \
  && echo "PYTHON_SYNTAX=PASS" \
  || echo "PYTHON_SYNTAX=FAIL"
echo

echo "## 5. Python server candidates"
find . -type f \( \
  -name 'server.py' -o \
  -name '*server*.py' -o \
  -name '*runtime*.py' \
\) \
-not -path './.git/*' \
-not -path './node_modules/*' \
-not -path './venv/*' \
-not -path './.venv/*' \
| sort
echo

echo "## 6. IMA master runtime locations"
find . -type f \( \
  -name 'ima_master_runtime.py' -o \
  -name 'ima_master_runtime*.py' \
\) \
-not -path './.git/*' \
| sort
echo

echo "## 7. Frontend"
if [ -f ima-ui/package.json ]; then
  cd ima-ui
  echo "IMA_UI_PRESENT=YES"
  node --version
  npm --version
  npm run build
  UI_RESULT=$?
  cd "$ROOT"
  if [ "$UI_RESULT" -eq 0 ]; then
    echo "IMA_UI_BUILD=PASS"
  else
    echo "IMA_UI_BUILD=FAIL"
  fi
else
  echo "IMA_UI_PRESENT=NO"
fi
echo

echo "## 8. Git integrity"
git diff --check
DIFF_RESULT=$?

if [ "$DIFF_RESULT" -eq 0 ]; then
  echo "GIT_DIFF_CHECK=PASS"
else
  echo "GIT_DIFF_CHECK=FAIL"
fi
echo

echo "## 9. Repository status after diagnostics"
git status --short
echo

echo "## 10. Decision"
if [ "$DIFF_RESULT" -eq 0 ]; then
  echo "No destructive changes were made."
  echo "No existing user changes were staged."
  echo "No commit or push was performed."
  echo
  echo "NEXT_STATE=DIAGNOSED"
else
  echo "Git whitespace/errors detected."
  echo "No destructive changes were made."
  echo "NEXT_STATE=REQUIRES_REPAIR"
fi

echo
echo "REPORT=$REPORT"
echo "BACKUP=$BACKUP"
