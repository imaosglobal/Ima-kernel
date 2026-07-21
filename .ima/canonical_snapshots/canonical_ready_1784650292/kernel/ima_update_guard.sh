#!/usr/bin/env bash

set -e

echo "[IMA SAFE UPDATE]"

git pull

# חשוב: force CI mode
export IMA_MODE=ci

bash ima_pipeline_final.sh

echo "[UPDATE DONE - SAFE EXIT]"
