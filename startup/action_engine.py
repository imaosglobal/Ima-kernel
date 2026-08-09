from pathlib import Path

class ActionEngine:

    def read_file(self, name):
        for p in Path(".").rglob(name):
            if ".git" not in str(p):
                return p.read_text(errors="ignore")[:3000]

        return "לא נמצא קובץ כזה"

    def list_folder(self, folder="."):
        p = Path(folder)
        if not p.exists():
            return "התיקייה לא קיימת"

        return "\n".join(str(x) for x in list(p.iterdir())[:50])
