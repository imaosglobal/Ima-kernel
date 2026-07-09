#!/usr/bin/env bash

MODE="$1"

if [ "$MODE" = "update" ]; then
  echo "[GUARD] UPDATE MODE ENABLED"
  export IMA_MODE=update
elif [ "$MODE" = "release" ]; then
  echo "[GUARD] RELEASE MODE ENABLED"
  export IMA_MODE=release
else
  echo "[GUARD] UNKNOWN MODE"
  exit 1
fi
