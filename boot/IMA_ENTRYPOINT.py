#!/usr/bin/env python3
"""
IMA ENTRYPOINT REDIRECT

Canonical entry:
IMA_START.py

No independent boot logic allowed.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))

from IMA_START import run


if __name__ == "__main__":
    sys.exit(run())
