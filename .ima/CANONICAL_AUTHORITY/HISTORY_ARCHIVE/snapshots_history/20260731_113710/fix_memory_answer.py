from pathlib import Path

p=Path("ima_master_runtime.py")
s=p.read_text(encoding="utf-8")

# מוסיף מנגנון תשובה לזיכרון
if "def memory_direct_answer" not in s:

    insert = r'''

def memory_direct_answer(message, memory):
    if not isinstance(message,str):
        return None

    m=message.strip()

    prefs=[]

    try:
        if isinstance(memory,dict):
            for k,v in memory.items():
                if k=="preference":
                    if isinstance(v,dict):
                        prefs.append(str(v.get("value","")))
                    else:
                        prefs.append(str(v))
    except Exception:
        pass

    if "מה אני אוהב" in m and prefs:
        return "אני זוכרת שאתה אוהב " + ", ".join(prefs)

    return None

'''

    s=s.replace("IMA=IMAMaster()", insert+"\n\nIMA=IMAMaster()")


# אחרי memory_context = get_context()
old="memory_context = get_context()"

new="""memory_context = get_context()

        direct_memory = memory_direct_answer(
            message,
            memory_context
        )

        if direct_memory:
            return {
                "time":time.time(),
                "message":message,
                "response":direct_memory,
                "memory_context":memory_context,
                "connections":{
                    "memory":True,
                    "brain":True
                }
            }
"""

if old in s and "direct_memory = memory_direct_answer" not in s:
    s=s.replace(old,new,1)


p.write_text(s,encoding="utf-8")

print("memory direct answer installed")
