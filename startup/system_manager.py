from pathlib import Path
from datetime import datetime


class SystemManager:

    def read(self, path):
        p = Path(path)

        if not p.exists():
            return f"לא נמצא: {path}"

        return p.read_text(errors="ignore")[:5000]


    def delete(self, path):
        p = Path(path)

        if not p.exists():
            return f"לא נמצא: {path}"

        backup = p.with_suffix(
            p.suffix + ".backup_" +
            datetime.now().strftime("%Y%m%d_%H%M%S")
        )

        backup.write_text(
            p.read_text(errors="ignore"),
            encoding="utf-8"
        )

        p.unlink()

        return f"נמחק: {path}\nגיבוי: {backup}"


    def replace(self, path, old, new):
        p = Path(path)

        if not p.exists():
            return f"לא נמצא: {path}"

        data = p.read_text(errors="ignore")

        if old not in data:
            return "טקסט לא נמצא"

        backup = p.with_suffix(
            p.suffix + ".backup_" +
            datetime.now().strftime("%Y%m%d_%H%M%S")
        )

        backup.write_text(data, encoding="utf-8")

        p.write_text(
            data.replace(old, new),
            encoding="utf-8"
        )

        return f"עודכן: {path}"
