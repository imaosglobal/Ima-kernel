#!/usr/bin/env bash

STAMP=$(date +%s)

git add -A

if git diff --cached --quiet; then
    echo "[SNAPSHOT] nothing to commit"
    exit 0
fi

git commit -m "snapshot: $STAMP"
echo "[SNAPSHOT] committed $STAMP"
