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

p.write_text(text)

