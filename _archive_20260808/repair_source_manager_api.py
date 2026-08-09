from pathlib import Path

p=Path("learning/source_manager.py")

text=p.read_text(encoding="utf8")

text=text.replace(
'headers={"User-Agent":"IMA-Knowledge-Agent"}',
'headers={"User-Agent":"IMA-Knowledge-Agent/1.0 (contact: ima@example.com)","Accept":"application/json"}'
)

text=text.replace(
'https://he.wikipedia.org/api/rest_v1/page/summary/',
'https://he.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=true&explaintext=true&format=json&titles='
)

p.write_text(text,encoding="utf8")

print("SOURCE API PATCHED")
