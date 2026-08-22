import json
from pathlib import Path

class IMA_UserProfile:
    def __init__(self):
        p = Path("../memory.json")
        default = {"users": {}, "conversations": [], "facts": {}}
        try:
            data = json.loads(p.read_text()) if p.exists() else default
            if not isinstance(data, dict): data = default
        except:
            data = default
        self.memory = data
        p.write_text(json.dumps(self.memory))

# הוצאנו את השורה הזאת מפה: ima_profile = IMA_UserProfile()
# עכשיו נטען רק כשצריך בפנים
