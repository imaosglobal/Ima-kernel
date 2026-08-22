from pathlib import Path

old = "module_registry"
new = "module_registry"

files = []

for p in Path(".").rglob("*"):
    if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts:
        try:
            text = p.read_text(encoding="utf-8")
            if old in text:
                files.append(p)
        except:
            pass

for f in files:

for f in files:
    text = f.read_text(encoding="utf-8")
    text = text.replace(old, new)
    text = text.replace(
        "learning_module_registry",
        "learning_module_registry"
    )
    text = text.replace(
        "IMA MODULE REGISTRY",
        "IMA MODULE REGISTRY"
    )
    text = text.replace(
        "MODULE REGISTRY SAVED",
        "MODULE REGISTRY SAVED"
    )
    f.write_text(text, encoding="utf-8")

old_file = Path("learning/module_registry.py")
new_file = Path("learning/module_registry.py")

if old_file.exists():
    old_file.rename(new_file)


