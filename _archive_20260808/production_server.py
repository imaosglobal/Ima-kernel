#!/usr/bin/env python3
import os
import sys

print("=== IMA PRODUCTION ENTRYPOINT ===", flush=True)
print("PORT=", os.environ.get("PORT"), flush=True)

server="api/server.py"

if not os.path.exists(server):
    print("[FAIL] api/server.py missing", flush=True)
    sys.exit(1)

print("[OK] launching API", flush=True)

os.execvp(
    "python3",
    ["python3", "-u", server]
)
