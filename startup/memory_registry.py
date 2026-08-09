from pathlib import Path
import json
from datetime import datetime


class MemoryRegistry:

    def __init__(self):
        self.path = Path(".ima/memory/file_registry.json")
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def register(self, file_path):
        data = []

        if self.path.exists():
            try:
                data = json.loads(
                    self.path.read_text(encoding="utf-8")
                )
            except Exception:
                data = []

        data.append({
            "file": str(file_path),
            "created": datetime.now().isoformat(),
            "status": "new"
        })

        self.path.write_text(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        return "נרשם בזיכרון IMA"
