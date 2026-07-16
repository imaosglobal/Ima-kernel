from pathlib import Path

p=Path("founder/core/founder_core.py")
text=p.read_text()

old='''        advice = advise(memory)'''

new='''        advice = advise(
            memory.get("query","founder_cycle")
        )'''

if old in text:
    text=text.replace(old,new,1)
else:
    print("[WARN] advisor call not found")

p.write_text(text)

print("[OK] FounderCore advisor API fixed")
