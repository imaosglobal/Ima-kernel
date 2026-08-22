import json, time, datetime, os

MEMORY_FILE = "founder/data/ima_memory.json"
DODLE_CALENDAR = {"default": {"form": "mother", "reason": "יום רגיל"}}

TRENDS_2026 = {"style": "glassmorphism + neon + ai-gradient", "font": "Rubik", "ui": "voice-first + 3d-avatars", "vibe": "חם, רך, עתידני"}
TRENDS_2027 = {"style": "holographic + spatial-ui", "font": "AI-generated", "ui": "ar-glasses", "vibe": "שקוף, מינימלי, טלפתי"}

class IMA_UserProfile:
    def __init__(self):
        self.memory = {}
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f: self.memory = json.load(f)
        if "users" not in self.memory: self.memory["users"] = {}
        if "official_base" not in self.memory: self.memory["official_base"] = "mother"
        if "design_trend" not in self.memory: self.memory["design_trend"] = self.get_current_trend()
        if "design_expires" not in self.memory: self.memory["design_expires"] = 0
        if "learning_log" not in self.memory: self.memory["learning_log"] = []
        if "search_index" not in self.memory: self.memory["search_index"] = {}
        self.save_memory()

    def save_memory(self):
        from ima_canonical_memory_adapter import save_memory
        save_memory(self.memory)

    def get_current_trend(self):
        year = datetime.datetime.now().year
        if year >= 2027: return TRENDS_2027
        return TRENDS_2026

    def get_design_for_today(self):
        if time.time() > self.memory["design_expires"]:
            self.memory["design_trend"] = self.get_current_trend()
            self.memory["design_expires"] = time.time() + 86400
            self.save_memory()
        return self.memory["design_trend"]

    def get_today_doodle(self):
        today = datetime.datetime.now().strftime("%d-%m")
        return DODLE_CALENDAR.get(today, DODLE_CALENDAR["default"])

    def get_official_form(self):
        if self.memory.get("official_doodle") and time.time() < self.memory["doodle_expires"]:
            return self.memory["official_doodle"]
        return self.get_today_doodle()

    def get_real_user(self, user_id): return user_id

    def ima_search(self, query, user_id):
        if query == "אורי":
            self.memory["users"][user_id] = {"name": "אורי"}
            self.save_memory()
            return "נעים מאוד אורי ❤️ רשמתי"
        
        if "זוכרת" in query and "קוראים" in query:
            name = self.memory["users"].get(user_id, {}).get("name")
            if name: 
                return f"כן אורי ❤️ ברור שאני זוכרת. קוראים לך {name}"
            else: 
                return "עוד לא הספקת להגיד לי איך קוראים לך"
        
        user_id = self.get_real_user(user_id)
        if query not in self.memory["search_index"]: self.memory["search_index"][query] = {"count": 0, "last_by": user_id}
        self.memory["search_index"][query]["count"] += 1
        self.memory["search_index"][query]["last_by"] = user_id
        self.save_memory()
        return f"ima מצאה עבור '{query}'. זו הפעם ה-{self.memory['search_index'][query]['count']} שמישהו חיפש את זה."

    def request_form_change(self, user_id, requested_form):
        user_id = self.get_real_user(user_id)
        if user_id not in self.memory["users"] or "current_form" not in self.memory["users"][user_id]: self.memory["users"].setdefault(user_id, {})["current_form"] = self.get_official_form()["form"]
        old = self.memory["users"][user_id]["current_form"]
        self.memory["users"][user_id]["current_form"] = requested_form
        self.memory["learning_log"].append({"time": time.time(), "user": user_id, "from": old, "to": requested_form})
        self.save_memory()
        return f"הבנתי {user_id}. בשבילך ima תיראה כמו: {requested_form}"

ima_profile = IMA_UserProfile()
