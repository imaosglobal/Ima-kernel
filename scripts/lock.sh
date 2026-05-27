#!/bin/bash

source "$HOME/ima_kernel/runtime/env.sh"

mkdir -p "$IMA_LOCKS"

LOCKFILE="$IMA_LOCKS/service.lock"

exec 9>"$LOCKFILE"

if ! flock -n 9; then
  exit 1
fi

trap 'rm -f "$LOCKFILE"' EXIT
