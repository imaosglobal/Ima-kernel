from pathlib import Path

p=Path("learning/source_manager.py")

text=p.read_text(encoding="utf8")

start=text.index("def wikipedia_search")
end=text.index("def get_real_source")

new=r'''
def normalize_term(question):
    term=question.strip()
    term=term.replace("מה זה ","")
    term=term.replace("מהי ","")
    term=term.replace("?","")
    return term.strip()


def wikipedia_search(question):

    try:
        term=normalize_term(question)

        for lang in ["he","en"]:

            url=(
                f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/"
                +
                term.replace(" ","_")
            )

            req=urllib.request.Request(
                url,
                headers={
                    "User-Agent":"IMA-Knowledge-Agent"
                }
            )

            with urllib.request.urlopen(req,timeout=8) as r:
                data=json.loads(
                    r.read().decode("utf8")
                )

            if data.get("extract"):
                return {
                    "content":data["extract"],
                    "source":f"wikipedia_{lang}",
                    "confidence":0.85
                }

    except Exception:
        pass

    return None


'''

text=text[:start]+new+text[end:]

p.write_text(text,encoding="utf8")

