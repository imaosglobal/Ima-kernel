class PersonaEngine:

    def select(self, user_type):
        return {
            "mode": user_type,
            "system": "IMA"
        }

engine = PersonaEngine()
