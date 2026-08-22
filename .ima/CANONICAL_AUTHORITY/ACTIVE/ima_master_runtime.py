import json
from pathlib import Path

class IMA_UserProfile:
    def __init__(self):
        p = Path("../memory.json")
        if not p.exists(): p.write_text('{"users": {}}')
        data = json.loads(p.read_text())
        # אם בטעות זה רשימה - נהפוך למילון
        if isinstance(data, list): data = {"users": {}}
        self.memory = data
