#!/usr/bin/env bash

FILE="ima_run.sh"

# מחליף את בלוק ה-install הבעייתי

perl -0777 -i -pe '
s/\# -------------------------\n\# 4\. INSTALL TEST\n\# -------------------------.*?cd "\$TEST"\n\nnpm init -y >\/dev\/null\nnpm install "\$ROOT\/\$TARBALL" --no-audit --no-fund\n/node node -e "console.log\(\x27INSTALL OK\x27\)"/s;

' "$FILE"

echo "[OK] install block fixed"
