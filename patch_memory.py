import re

with open('ima_system.py', 'r', encoding='utf-8') as f:
    code = f.read()

# מחפש את הפונקציה load_memory ומחליף אותה
old_func = r'def load_memory\(\):.*?return mem'
new_func = '''def load_memory():
    import json
    from pathlib import Path
    p = Path(".ima/memory.json")
    p.parent.mkdir(exist_ok=True)
    default = {"users": {}, "conversations": [], "facts": {}, "last_language": "he"}
    try:
        if p.exists():
            data = json.loads(p.read_text())
            if not isinstance(data, dict):
                raise ValueError("corrupted")
            return data
    except:
        pass
    p.write_text(json.dumps(default))
    return default'''

code = re.sub(old_func, new_func, code, flags=re.DOTALL)
with open('ima_system.py', 'w', encoding='utf-8') as f:
    f.write(code)
