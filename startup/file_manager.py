from pathlib import Path

class FileManager:

    def delete(self, path):

        target = Path(path)

        if not target.exists():
            return f"לא נמצא: {path}"

        target.unlink()

        return f"נמחק: {path}"

    def remove_text(self, path, text):

        target = Path(path)

        if not target.exists():
            return f"לא נמצא: {path}"

        data = target.read_text(errors="ignore")

        data = data.replace(text, "")

        target.write_text(data)

        return f"הוסר טקסט מתוך: {path}"
