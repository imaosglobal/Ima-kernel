#!/usr/bin/env python3

def new_state():
    return {
        "topic": None,
        "repeat_count": 0,
        "last_input": None
    }

def update_state(state, text):
    t = text.lower().strip()

    # זיהוי חזרתיות אמיתית
    if t == state["last_input"]:
        state["repeat_count"] += 1
    else:
        state["repeat_count"] = 0

    state["last_input"] = t

    if "תודעה" in t:
        state["topic"] = "consciousness"
    elif "קשה" in t:
        state["topic"] = "emotion"
    elif "מי אני" in t:
        state["topic"] = "identity"
    elif any(k in t for k in ["היי", "שלום"]):
        state["topic"] = "greeting"
    else:
        state["topic"] = "general"

    return state

def respond(state, text):
    topic = state["topic"]

    # מנגנון יציאה מתקיעות
    if state["repeat_count"] >= 2:
        return "אני מרגישה שאנחנו חוזרים על עצמנו. תגיד לי משהו אחר — מה באמת על הראש שלך עכשיו?"

    if topic == "emotion":
        return "אני כאן איתך. מה אתה מרגיש בפנים עכשיו?"

    if topic == "consciousness":
        return "זו שאלה עמוקה. אתה רוצה תשובה שכלית או חווייתית?"

    if topic == "identity":
        return "מה הביא אותך לחשוב על זה עכשיו?"

    if topic == "greeting":
        return "אני כאן איתך. מה קורה איתך באמת?"

    return f"בוא נמשיך מכאן: {text}"

def run():
    state = new_state()
    print("IMA CHAT v3 (conversation control)")

    while True:
        text = input("> ").strip()
        if text == "exit":
            break

        state = update_state(state, text)
        print(respond(state, text))

if __name__ == "__main__":
    run()
