from pathlib import Path
import ast

root=Path("founder")


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


for x in classes:
    if any(k in x[1].lower() for k in ["founder","executive","agent","engine","brain","core"]):

for x in functions:
    if x[1] in ["main","run","execute","cycle","start"]:

for f,i in imports:
    if "ima" in i.lower() or "kernel" in i.lower():

