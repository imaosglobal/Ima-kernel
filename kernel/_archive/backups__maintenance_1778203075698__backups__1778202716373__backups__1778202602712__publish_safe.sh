#!/usr/bin/env bash

set -e

echo "[PIPE] starting safe publish..."

bash ~/ima_core/kernel/prepublish_check.sh

echo "[PIPE] version bump..."
npm version patch -m "auto: safe release"

echo "[PIPE] publishing..."
npm publish

echo "[PIPE] DONE"
