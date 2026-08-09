from pathlib import Path
from datetime import datetime
class PitchEngine:
    def __init__(self):
        self.root = Path(".")
        self.output = Path("startup/IMA_pitch_deck.md")
        self.memory_paths = [Path(".ima/memory"), Path(".ima/snapshots")]
    def scan_materials(self):
        files = []
        for f in self.root.rglob("*"):
            if f.is_file():
                path = str(f)
                if any(x in path for x in [".git","node_modules","__pycache__"]): continue
                if any(x in f.name.lower() for x in ["pitch","deck","identity","vision","readme","toolbox"]): files.append(path)
        return files[:30]
    def has_real_deck(self, files):
        keywords = ["problem","solution","market","team","ask"]; score = 0
        for file in files:
            try: text = Path(file).read_text(errors="ignore").lower(); [score:=score+1 for k in keywords if k in text]
            except: pass
        return score >= 5
    def build_deck(self):
        materials = self.scan_materials()
        status = "נמצא חומר Deck משמעותי קיים" if self.has_real_deck(materials) else "אין Deck מלא. נוצר Draft חדש."
        self.output.parent.mkdir(exist_ok=True)
        content = f"# IMA Investor Pitch Deck v0.1\nנוצר: {datetime.now()}\nמצב:\n{status}\n\n## Problem\nיזמים צריכים שותף AI אישי.\n## Solution\nIMA OS - מערכת AI עם זיכרון ואוטומציה.\n## Ask\n500K Pre-seed\n## Sources scanned\n" + "\n".join([f"- {m}" for m in materials])
        self.output.write_text(content, encoding="utf-8")
        for p in self.memory_paths: p.mkdir(parents=True, exist_ok=True); (p / "IMA_pitch_deck_backup.md").write_text(content, encoding="utf-8")
        return f"בניית Investor Deck הושלמה 💛\n{status}\n\nקובץ: {self.output}\nנסרקו {len(materials)} מקורות."
