#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"
YEAR="$(date +%Y)"
OWNER="${IMA_OWNER_NAME:-IMA Founder}"
PROJECT="IMA"

mkdir -p legal governance .github

cat > COPYRIGHT.md <<EOF
# Copyright and Authorship

Copyright (c) ${YEAR} ${OWNER}.

The IMA project, its original source code, documentation, architecture,
original designs, naming, and original creative works are protected by
applicable copyright and other intellectual-property laws.

No ownership transfer is granted by this repository unless expressly stated
in a separate written agreement signed by the rights holder.

All rights not expressly granted by the applicable license are reserved.
EOF

cat > NOTICE <<EOF
${PROJECT} — NOTICE

Original rights holder: ${OWNER}
Copyright: ${YEAR}

This notice does not replace the applicable software license.
Third-party components remain subject to their own licenses.
EOF

cat > LICENSE.md <<'EOF'
# IMA License Notice

This repository is released under the license stated in the repository's
official LICENSE file.

Copyright ownership is retained by the rights holder.
A license to use, copy, modify, or distribute software is not the same as
a transfer of copyright ownership.

No trademark rights, patent rights, or ownership rights are granted except
where expressly stated by the applicable license.

Third-party components remain subject to their original licenses.
EOF

cat > RIGHTS_AND_SUCCESSION.md <<'EOF'
# Rights, Succession, and Stewardship

The project should maintain a documented chain of authorship, provenance,
and stewardship.

The rights holder may establish separate legally valid instruments for:
- copyright ownership and licensing;
- trademark ownership;
- patent rights where applicable;
- estate and succession planning;
- trusts or foundations where legally available;
- governance and stewardship of the project;
- rights of heirs and successors.

This document is not itself a will, trust, contract, or legal instrument.
Local law governs enforceability.

No software mechanism can guarantee perpetual ownership, universal
enforceability in every jurisdiction, or rights beyond applicable law.
EOF

cat > CONTRIBUTING.md <<'EOF'
# Contributing

By contributing, contributors must follow the contribution terms specified
by the project maintainers and any applicable contributor agreement.

Contributors retain rights they legally retain unless a valid written
agreement states otherwise.

Do not submit confidential information, secrets, credentials, or material
that you do not have the right to contribute.
EOF

cat > SECURITY.md <<'EOF'
# Security

Never commit passwords, API keys, private keys, tokens, personal data, or
other secrets.

Security reports should be handled privately before public disclosure.
EOF

cat > .github/SECURITY_CHECK.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

echo "== SECRET SCAN =="

patterns='(BEGIN .* PRIVATE KEY|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|password[[:space:]]*[:=]|api[_-]?key[[:space:]]*[:=])'

if grep -RInE \
  --exclude-dir=.git \
  --exclude='*.pyc' \
  --exclude='*.glb' \
  --exclude='*.lock' \
  "$patterns" .; then
  echo "SECRET_SCAN=FAIL"
  exit 1
fi

echo "SECRET_SCAN=PASS"
EOF

chmod +x .github/SECURITY_CHECK.sh

cat > .github/workflows/integrity.yml <<'EOF'
name: IMA Integrity

on:
  push:
  pull_request:

jobs:
  integrity:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Secret scan
        run: bash .github/SECURITY_CHECK.sh

      - name: Python syntax check
        run: |
          python3 -m py_compile ima_master_runtime.py

      - name: Runtime hash
        run: |
          sha256sum ima_master_runtime.py
EOF

git add COPYRIGHT.md NOTICE LICENSE.md RIGHTS_AND_SUCCESSION.md \
  CONTRIBUTING.md SECURITY.md .github

git commit -m "establish global rights provenance succession and integrity framework"

echo
echo "IMA RIGHTS FRAMEWORK CREATED"
echo "COMMIT:"
git log -1 --oneline
echo
echo "STATUS:"
git status --short
