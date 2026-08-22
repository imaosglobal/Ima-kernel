from pathlib import Path

p=Path("learning/sources/source_inspector.py")

text=p.read_text(encoding="utf8")

text=text.replace(
'''elif r.status in [301,302,403]:
                score += 20
            elif r.status in [301,302,403]:
                score += 20''',
'''elif r.status in [301,302,403]:
                score += 20'''
)

text=text.replace(
'''except Exception:
        score -= 20''',
'''except Exception:
        score -= 10'''
)

text=text.replace(
'''result["trust_score"]=score''',
    result["trust_score"]=score'''
)

p.write_text(text,encoding="utf8")

