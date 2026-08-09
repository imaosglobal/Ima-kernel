from pathlib import Path

p=Path("ima_master_runtime.py")
s=p.read_text(encoding="utf-8")

start=s.find("        # FORCE_MEMORY_PRIORITY")

if start != -1:
    end=s.find("        # END_FORCE_MEMORY_PRIORITY", start)

    if end != -1:
        end += len("        # END_FORCE_MEMORY_PRIORITY")

        replacement=r'''
        # FORCE_MEMORY_PRIORITY_FIXED

        def deep_find_preferences(obj):
            found=[]

            if isinstance(obj,dict):
                for k,v in obj.items():

                    if k=="preference":
                        if isinstance(v,dict):
                            value=v.get("value","")
                            if value:
                                found.append(str(value))
                        elif v:
                            found.append(str(v))

                    found.extend(
                        deep_find_preferences(v)
                    )

            elif isinstance(obj,list):
                for item in obj:
                    found.extend(
                        deep_find_preferences(item)
                    )

            return found


        forced_prefs=deep_find_preferences(
            memory_context
        )


        if "מה אני אוהב" in message and forced_prefs:

            clean_pref=[]

            for x in forced_prefs:
                if x not in clean_pref:
                    clean_pref.append(x)

            return {
                "time":time.time(),
                "message":message,
                "response":
                    "אני זוכרת שאתה אוהב "
                    + ", ".join(clean_pref),
                "memory_context":memory_context,
                "connections":{
                    "memory":True,
                    "brain":True,
                    "mother":True
                }
            }

        # END_FORCE_MEMORY_PRIORITY
'''

        s=s[:start]+replacement+s[end:]

        p.write_text(
            s,
            encoding="utf-8"
        )

        print("MEMORY FLOW REPAIRED")
    else:
        print("END MARKER NOT FOUND")
else:
    print("PATCH NOT FOUND")
