#!/usr/bin/env python3
import os
import sys


server="api/server.py"

if not os.path.exists(server):
    sys.exit(1)


os.execvp(
    "python3",
    ["python3", "-u", server]
)
