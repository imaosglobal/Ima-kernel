from pathlib import Path

p = Path("ima_system.py")
s = p.read_text()

insert = r'''

# -------------------------
# LLM CONNECTOR
# -------------------------
def llm_answer(question, events):
    """
    Placeholder for real language model.
    Priority:
    1. OpenAI API
    2. Local model
    3. Emotional fallback
    """
    import os

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role":"system",
                        "content":
                        "את IMA. את אמא טכנולוגית. "
                        "עני בעברית טבעית, אנושית, חמה ועמוקה. "
                        "אל תישמעי כמו תוכנה."
                    },
                    {
                        "role":"user",
                        "content":question
                    }
                ]
            )

            return {
                "text": response.choices[0].message.content,
                "confidence": 0.95
            }

        except Exception as e:
            pass

    return None
'''

if "def llm_answer" not in s:
    s += insert

old = '''def answer(question, events):'''

new = '''def answer(question, events):

    model_result = llm_answer(question, events)
    if model_result:
        return model_result
'''

if old in s and "model_result = llm_answer" not in s:
    s=s.replace(old,new)

p.write_text(s)
print("LLM layer added")
