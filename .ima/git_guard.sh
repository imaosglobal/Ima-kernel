#!/usr/bin/env bash

echo "[GIT GUARD] staging all changes..."

git add -A

if git diff --cached --quiet; then
    echo "[GIT GUARD] nothing to commit"
    exit 1
fi

echo "[GIT GUARD] ready"
