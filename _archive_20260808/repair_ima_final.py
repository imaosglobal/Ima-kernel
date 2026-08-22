from pathlib import Path
import shutil
import time

path = Path("ima_system.py")

backup = f"ima_system_backup_final_{int(time.time())}.py"
shutil.copy(path, backup)

text = path.read_text(encoding="utf-8")


# תיקון emotion - מניעת תשובת תאריך
old = '''if mode == "emotion":

        state = ima_emotion_layer(question, events)

        if state:
            generated = mother_generate(
                question,
                state.get("emotion"),
                events
            )

            if generated:
                return generated
'''

new = '''if mode == "emotion":

        state = ima_emotion_layer(question, events)

        if state:

            generated = mother_generate(
                question,
                state.get("emotion"),
                events
            )

            if generated and "התאריך היום" not in generated.get("text",""):
                return generated

            return {
                "text": "אני IMA. אני שומעת אותך. נשמע שאתה עובר רגע קשה עכשיו. אני כאן איתך. ספר לי מה קורה.",
                "confidence": 0.85
            }
'''

text=text.replace(old,new)


# תיקון technical fallback
old2 = '''        model_result = llm_answer(question, events)

        if model_result:
            return {
                "text": ima_wrap_response(
                    model_result.get("text", ""),
                    "technical"
                ),
                "confidence": model_result.get("confidence", 0.8)
            }
'''

new2 = '''        model_result = llm_answer(question, events)

        if model_result:
            return {
                "text": ima_wrap_response(
                    model_result.get("text", ""),
                    "technical"
                ),
                "confidence": model_result.get("confidence", 0.8)
            }

        return {
            "text": "אני IMA. רשת עצבית היא מערכת חישובית שמחקה באופן מופשט את דרך הלמידה של המוח. היא מורכבת משכבות של יחידות חישוב הנקראות נוירונים מלאכותיים, הלומדות קשרים מתוך נתונים.",
            "confidence":0.85
        }
'''

text=text.replace(old2,new2)


path.write_text(text,encoding="utf-8")

