#!/data/data/com.termux/files/usr/bin/bash
set -e

cd "$(dirname "$0")"

python3 canonical_guard.py

exec "$@"
