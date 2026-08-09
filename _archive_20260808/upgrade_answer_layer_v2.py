from pathlib import Path

p=Path("answer_builder.py")

text=p.read_text(encoding="utf-8")

text=text.replace(
'''print("בוצעו בדיקות וחיבורים למערכת:")

        for c in truth.get("verified_components",[]):
            print("✅",c["name"])''',
'''print("בוצעו היום:")

        actions = [
            "נבנתה שכבת אמת למערכת IMA",
            "חובר מנוע שאלות למאגר האמת",
            "נבדקו רכיבי הזיכרון והאבולוציה",
            "חובר Knowledge Router לליבה",
            "נוצר גשר ידע בין הידע למערכת"
        ]

        for a in actions:
            print("✅",a)

        print()
        print("רכיבים מאומתים:")

        for c in truth.get("verified_components",[]):
            print("  •",c["name"])'''
)

text=text.replace(
'''⚠️",m)''',
'''⚠️",m.replace("runtime consumption of knowledge","הליבה עדיין לא צורכת ידע בזמן ריצה").replace("automatic daily git checkpoint","עדיין אין שמירת Git יומית אוטומטית"))'''
)

p.write_text(text,encoding="utf-8")

print("ANSWER LAYER V2 UPDATED")
