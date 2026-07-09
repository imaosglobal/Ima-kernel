#!/usr/bin/env bash

set -e

echo "[PIPELINE] build start"

# רק pack + version + publish
npm pack
echo "[PIPELINE] pack done"

