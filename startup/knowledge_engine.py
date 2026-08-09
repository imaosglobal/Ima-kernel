from pathlib import Path
class KnowledgeEngine:
    def __init__(self):
        self.memory = {}
        self.load_all()
    def load_all(self):
        for f in Path(".").rglob("*.md"):
            if ".git" not in str(f):
                try: self.memory[str(f)] = f.read_text(errors="ignore")[:1000]
                except: pass
    def answer(self, q):
        q = q.lower()
        if "toolbox" in q: return self.memory.get("toolbox_knowledge.md", "אין toolbox")
        if "deck" in q: return self.memory.get("startup/IMA_pitch_deck.md", "אין deck")
        return f"יודעת {len(self.memory)} קבצים 💛\n" + "\n".join(list(self.memory.keys())[:10])
