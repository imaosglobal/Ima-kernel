from pathlib import Path
import json
import time

files=list(Path(".").rglob("user_memory.json"))

for f in files:
    try:
        data=json.loads(f.read_text(encoding="utf-8"))

        changed=False

        def clean(v):
            global changed

            if isinstance(v,dict):
                for k in list(v.keys()):
                    if k=="last_response":
                        val=v[k]
                        if isinstance(val,dict):
                            text=val.get("value","")
                            if isinstance(text,str):
                                if (
                                    "זיכרון משתמש:" in text or
                                    "הקשר משתמש:" in text or
                                    "הודעת משתמש:" in text
                                ):
                                    v[k]={
                                        "value":"",
                                        "time":time.time()
                                    }
                                    changed=True

                    else:
                        clean(v[k])

            elif isinstance(v,list):
                for x in v:
                    clean(x)

        clean(data)

        if changed:
            f.write_text(
                json.dumps(
                    data,
                    ensure_ascii=False,
                    indent=2
                ),
                encoding="utf-8"
            )
            print("cleaned:",f)

    except Exception:
        pass

print("DONE")
