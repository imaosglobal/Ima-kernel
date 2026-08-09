from pathlib import Path

p=Path("connectors/whatsapp/whatsapp_connector.py")
s=p.read_text(encoding="utf-8")

s=s.replace(
'''remember_user(
                    user_id,
                    "preference",
                    {
                        "value":pref
                    }
                )''',
'''remember_user(
                    user_id,
                    "preference",
                    pref
                )'''
)

s=s.replace(
'''if isinstance(pref,dict):
                    prefs.append(
                        pref.get("value","")
                    )

                elif isinstance(pref,list):
                    for p in pref:
                        if isinstance(p,dict):
                            prefs.append(
                                p.get("value","")
                            )''',
'''if isinstance(pref,dict):
                    value=pref.get("value","")

                    if isinstance(value,dict):
                        value=value.get("value","")

                    if value:
                        prefs.append(str(value))

                elif isinstance(pref,list):
                    for p in pref:
                        if isinstance(p,dict):
                            value=p.get("value","")
                            if value:
                                prefs.append(str(value))
                        else:
                            prefs.append(str(p))

                elif pref:
                    prefs.append(str(pref))'''
)

p.write_text(s,encoding="utf-8")
print("PREFERENCE STORAGE FIXED")
