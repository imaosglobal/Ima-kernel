#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"
YEAR="$(date +%Y)"
OWNER="${IMA_OWNER_NAME:-}"

if [[ -z "$OWNER" || "$OWNER" == "YOUR LEGAL NAME" ]]; then
  read -r -p "הזן את שמך החוקי המדויק כבעל זכויות היוצרים: " OWNER
fi

if [[ -z "$OWNER" ]]; then
  echo "ERROR: חסר שם בעל הזכויות"
  exit 1
fi

echo "== IMA RIGHTS FINALIZATION =="

cat > COPYRIGHT.md <<EOF
# IMA Copyright and Authorship

Copyright (c) ${YEAR} ${OWNER}.

The original IMA source code, original architecture, original documentation,
original designs, original naming, and other original creative works are
owned by the applicable rights holder, subject to applicable law and
third-party rights.

Copyright ownership is retained by the rights holder.
A license to use the software is not a transfer of copyright ownership.

Third-party components remain subject to their own licenses.
EOF

cat > LICENSE <<EOF
MIT License

Copyright (c) ${YEAR} ${OWNER}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY.
EOF

cat > RIGHTS_AND_SUCCESSION.md <<EOF
# IMA Rights, Provenance, and Succession

Rights holder:
${OWNER}

This repository documents authorship and provenance of the IMA project.

Copyright ownership is retained by the applicable rights holder. The open
source license grants permissions to use the software but does not transfer
copyright ownership.

Future succession, estate planning, trusts, foundations, trademarks,
patents, licensing structures, and inheritance arrangements must be created
through legally valid instruments applicable to the relevant jurisdiction.

This document is not a will, trust, contract, or substitute for legal advice.

No software repository can guarantee perpetual ownership or universal
enforceability in every jurisdiction. The project should preserve provenance,
copyright notices, license notices, signed releases, and legally valid
succession documents where applicable.
EOF

cat > .ima/RIGHTS_PROVENANCE.json <<EOF
{
  "project": "IMA",
  "rights_holder": "$(printf '%s' "$OWNER" | sed 's/"/\\"/g')",
  "copyright_year": "$YEAR",
  "copyright_ownership_transferred": false,
  "open_source_license": "MIT",
  "provenance_policy": "preserve_git_history_and_signed_releases",
  "succession_policy": "separate_ legally_valid_estate_and_succession_instruments_required",
  "universal_perpetual_guarantee": false,
  "third_party_rights": "preserved"
}
EOF

echo
echo "== VERIFY FILES =="
test -s LICENSE
test -s COPYRIGHT.md
test -s RIGHTS_AND_SUCCESSION.md
test -s .ima/RIGHTS_PROVENANCE.json
echo "RIGHTS_FILES=PASS"

echo
echo "== PYTHON CHECK =="
python3 -m py_compile ima_master_runtime.py
echo "PYTHON=PASS"

echo
echo "== IMA BOOT CHECK =="
python3 IMA_START.py 2>&1 | tail -30

echo
echo "== GIT STATUS =="
git status --short

echo
echo "== COMMIT =="
git add LICENSE COPYRIGHT.md RIGHTS_AND_SUCCESSION.md .ima/RIGHTS_PROVENANCE.json
git commit -m "finalize open source rights provenance and succession framework" || true

echo
echo "== REMOTE =="
git remote -v || true

if ! git remote get-url origin >/dev/null 2>&1; then
  echo
  echo "STOP: לא מוגדר remote בשם origin."
  echo "הוסף את כתובת המאגר שלך ואז הרץ:"
  echo "git remote add origin <YOUR_REPOSITORY_URL>"
  echo "git push -u origin main"
  exit 0
fi

echo
echo "== FINAL COMMIT =="
git log -1 --oneline

echo
echo "== PUSH =="
git push -u origin main

echo
echo "== PUBLISHED =="
git status --short
git log -1 --oneline
