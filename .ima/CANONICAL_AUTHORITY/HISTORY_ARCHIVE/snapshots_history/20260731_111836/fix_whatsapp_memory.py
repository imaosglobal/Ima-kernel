from pathlib import Path

p=Path("connectors/whatsapp/whatsapp_connector.py")
s=p.read_text(encoding="utf-8")

start=s.find("    def receive_message")
end=s.find("\n\n\n    def send_message", start)

if start == -1 or end == -1:
    print("receive_message block not found")
    exit()

new=r'''    def receive_message(self, user_id, message):

        remember_user(
            user_id,
            "last_message",
            message
        )

        memory = recall_user(user_id)


        # חילוץ העדפות אמיתי
        def extract_preferences(text):
            prefs=[]

            triggers=[
                "אני אוהב",
                "אני אוהבת",
                "אני אוהב את"
            ]

            for t in triggers:
                if t in text:
                    value=text.split(t,1)[1].strip()

                    if value:
                        prefs.append(value)

            return prefs


        preferences = extract_preferences(message)

        if preferences:

            for pref in preferences:
                remember_user(
                    user_id,
                    "preference",
                    {
                        "value":pref
                    }
                )


            return (
                "זכרתי שאתה אוהב "
                + ", ".join(preferences)
            )


        memory = recall_user(user_id)


        # תשובה ישירה מהזיכרון
        if "מה אני אוהב" in message:

            prefs=[]

            if isinstance(memory,dict):

                pref=memory.get("preference")

                if isinstance(pref,dict):
                    prefs.append(
                        pref.get("value","")
                    )

                elif isinstance(pref,list):
                    for p in pref:
                        if isinstance(p,dict):
                            prefs.append(
                                p.get("value","")
                            )


            prefs=[
                p for p in prefs
                if p
            ]


            if prefs:
                return (
                    "אני זוכרת שאתה אוהב "
                    + ", ".join(prefs)
                )


        prompt = f"""
שאלה:
{message}

זיכרון נקי:
{json.dumps(memory, ensure_ascii=False)}
"""


        result = IMA.ask(prompt)


        if isinstance(result,dict):
            reply=result.get(
                "response",
                ""
            )
        else:
            reply=str(result)


        # מניעת זיהום
        bad=[
            "את IMA.",
            "זיכרון משתמש:",
            "הודעה:"
        ]

        for b in bad:
            if b in reply:
                reply=reply.split(b)[0]


        reply=reply.strip()


        remember_user(
            user_id,
            "last_response",
            reply
        )


        return reply
'''

s=s[:start]+new+s[end:]

p.write_text(s,encoding="utf-8")

print("WHATSAPP MEMORY FLOW FIXED")
