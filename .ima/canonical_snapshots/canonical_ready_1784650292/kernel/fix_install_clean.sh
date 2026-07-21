#!/usr/bin/env bash

FILE="ima_run.sh"

awk '
BEGIN {skip=0}

# מחיקת בלוק install test הישן
/INSTALL TEST/ {skip=1}
skip==1 && /cd "\$ROOT"/ {skip=1}
skip==1 && /node -e/ {next}
skip==1 && /\}/ {skip=0; next}

# הדפס כל שאר השורות
skip==0 {print}
' "$FILE" > tmp.sh && mv tmp.sh "$FILE"

echo "[OK] removed broken install block"
