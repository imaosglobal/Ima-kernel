from pathlib import Path

base = Path("connectors/llm")
base.mkdir(parents=True, exist_ok=True)

files = {

"__init__.py": "",

"ollama.py": '''
import urllib.request
import json

def ask(prompt):
    try:
        data=json.dumps({
            "model":"llama3",
            "prompt":prompt,
            "stream":False
        }).encode()

        req=urllib.request.Request(
            "http://127.0.0.1:11434/api/generate",
            data=data,
            headers={"Content-Type":"application/json"}
        )

        r=urllib.request.urlopen(req,timeout=30)
        return json.loads(r.read()).get("response","")

    except Exception as e:
        return "[ollama unavailable] "+str(e)
''',

"openai.py": '''
import os

def ask(prompt):
    return "[openai connector pending]"
''',

"anthropic.py": '''
def ask(prompt):
    return "[anthropic connector pending]"
''',

"gemini.py": '''
def ask(prompt):
    return "[gemini connector pending]"
''',

"router.py": '''
from .ollama import ask as ollama

def ask_models(message):

    results={}

    results["ollama"]=ollama(message)

    return results
''',

"evaluator.py": '''
def evaluate(results):
    if not results:
        return ""

    for k,v in results.items():
        if v and not v.startswith("["):
            return v

    return ""
'''
}

for name,data in files.items():
    (base/name).write_text(data,encoding="utf-8")

print("LLM bridge created")
