#!/usr/bin/env python3
import os
import subprocess
import sys
import time

PORT = int(os.environ.get("PORT", "8080"))

print("=== IMA PRODUCTION SERVER ===")
print("PORT:", PORT)

server = "api/server.py"

if not os.path.exists(server):
    print("[FAIL] API missing")
    sys.exit(1)

print("[OK] Starting API")

os.execvp(
    "python3",
    ["python3", server]
)
