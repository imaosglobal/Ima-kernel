from pathlib import Path
import ast
from collections import defaultdict

root=Path("founder")

graph=defaultdict(list)

for f in root.rglob("*.py"):
    try:
        tree=ast.parse(f.read_text())
        name=str(f)

        for n in ast.walk(tree):
            if isinstance(n,ast.ImportFrom):
                if n.module and n.module.startswith("founder"):
                    graph[name].append(n.module)

    except:
        pass


print("=== FOUNDER DEPENDENCY GRAPH ===")

for src,targets in graph.items():
    print("\n",src)
    for t in targets:
        print("  ->",t)


print("\n=== MOST CONNECTED MODULES ===")

count=defaultdict(int)

for src,targets in graph.items():
    for t in targets:
        count[t]+=1

for k,v in sorted(count.items(),key=lambda x:x[1],reverse=True)[:20]:
    print(v,k)
