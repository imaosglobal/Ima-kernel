from pathlib import Path

p=Path("ima_master_runtime.py")
s=p.read_text(encoding="utf-8")

marker="# FORCE_MEMORY_PRIORITY"

if marker not in s:

    patch=r'''

        # FORCE_MEMORY_PRIORITY

        def extract_preferences(memory):
            prefs=[]

            try:
                if isinstance(memory,dict):

                    # מבנה רגיל
                    if "preference" in memory:
                        v=memory["preference"]

                        if isinstance(v,dict):
                            prefs.append(
                                str(v.get("value",""))
                            )
                        else:
                            prefs.append(str(v))

                    # חיפוש רקורסיבי
                    for value in memory.values():
                        if isinstance(value,dict):
                            prefs.extend(
                                extract_preferences(value)
                            )

            except Exception:
                pass

            return [
                x for x in prefs
                if x and len(x)>1
            ]


        forced_prefs=extract_preferences(
            memory_context
        )

        if "מה אני אוהב" in message and forced_prefs:

            return {
                "time":time.time(),
                "message":message,
                "response":
                    "אני זוכרת שאתה אוהב "
                    + ", ".join(forced_prefs),
                "memory_context":memory_context,
                "connections":{
                    "memory":True,
                    "brain":True
                }
            }

        # END_FORCE_MEMORY_PRIORITY

'''

    target="        intent = detect(message)"

    if target in s:
        s=s.replace(
            target,
            patch+"\n"+target,
            1
        )

        p.write_text(
            s,
            encoding="utf-8"
        )

        print("FORCE MEMORY PRIORITY INSTALLED")

    else:
        print("target missing")

else:
    print("already installed")

