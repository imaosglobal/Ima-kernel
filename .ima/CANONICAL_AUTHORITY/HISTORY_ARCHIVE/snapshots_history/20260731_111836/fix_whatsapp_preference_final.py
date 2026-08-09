from pathlib import Path

p=Path("connectors/whatsapp/whatsapp_connector.py")
s=p.read_text(encoding="utf-8")

start=s.find("        # חילוץ העדפות אמיתי")
end=s.find("        prompt =", start)

if start == -1 or end == -1:
    print("block not found")
    exit()

replacement=r'''        # MEMORY PREFERENCE ENGINE

        def find_text_values(obj):
            result=[]

            if isinstance(obj,dict):
                for k,v in obj.items():

                    if k=="value":
                        if isinstance(v,str):
                            result.append(v)

                    result.extend(
                        find_text_values(v)
                    )

            elif isinstance(obj,list):
                for x in obj:
                    result.extend(
                        find_text_values(x)
                    )

            return result


        if "אני אוהב" in message:

            value=message.split(
                "אני אוהב",
                1
            )[1].strip()

            if value:

                remember_user(
                    user_id,
                    "preference",
                    value
                )

                return (
                    "זכרתי שאתה אוהב "
                    + value
                )


        if "מה אני אוהב" in message:

            memory=recall_user(user_id)

            values=find_text_values(memory)

            values=[
                x for x in values
                if x not in [
                    "מה אני אוהב?",
                    "?",
                    ""
                ]
            ]

            if values:

                return (
                    "אני זוכרת שאתה אוהב "
                    + values[-1]
                )


'''

s=s[:start]+replacement+s[end:]

p.write_text(s,encoding="utf-8")

print("FINAL MEMORY PATCH INSTALLED")
