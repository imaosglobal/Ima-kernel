from pathlib import Path
from datetime import datetime

class FileBuilder:

    def create(self, path, content):
        target = Path(path)

        if target.exists():
            backup = target.with_suffix(
                target.suffix + ".backup_" +
                datetime.now().strftime("%Y%m%d_%H%M%S")
            )
            backup.write_text(
                target.read_text(errors="ignore"),
                encoding="utf-8"
            )

        target.parent.mkdir(parents=True, exist_ok=True)

        target.write_text(
            content,
            encoding="utf-8"
        )

        return f"נוצר קובץ: {target}"
