from pathlib import Path
import ast

root=Path("founder")

print("=== FOUNDER ARCHITECTURE SCAN ===")

files=list(root.rglob("*.py"))

classes=[]
functions=[]
imports=[]

for f in files:
    try:
        tree=ast.parse(f.read_text())
        for n in ast.walk(tree):
            if isinstance(n,ast.ClassDef):
                classes.append((str(f),n.name))
            if isinstance(n,ast.FunctionDef):
                functions.append((str(f),n.name))
            if isinstance(n,ast.Import) or isinstance(n,ast.ImportFrom):
                imports.append((str(f),ast.dump(n)))
    except:
        pass

print("FILES:",len(files))
print("CLASSES:",len(classes))
print("FUNCTIONS:",len(functions))

print("\n=== MAIN CLASSES ===")
for x in classes:
    if any(k in x[1].lower() for k in ["founder","executive","agent","engine","brain","core"]):
        print(x)

print("\n=== ENTRY FUNCTIONS ===")
for x in functions:
    if x[1] in ["main","run","execute","cycle","start"]:
        print(x)

print("\n=== POSSIBLE KERNEL LINKS ===")
for f,i in imports:
    if "ima" in i.lower() or "kernel" in i.lower():
        print(f,i)

