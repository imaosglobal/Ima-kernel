from pathlib import Path

p=Path("learning/sources/source_inspector.py")

text=p.read_text(encoding="utf8")

text=text.replace(
"import urllib.request",
"import urllib.request\nimport urllib.error"
)

text=text.replace(
'''    except Exception:
        score -= 10''',
'''    except urllib.error.HTTPError as e:
        if e.code in [301,302,403]:
            score += 20
        else:
            score -= 10

    except Exception:
        score -= 10'''
)

p.write_text(text,encoding="utf8")

