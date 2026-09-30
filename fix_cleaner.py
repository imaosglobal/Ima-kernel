import pathlib, re, json
base = pathlib.Path.home() / "Ima-kernel/.ima/muse_bridge"
for f in (base/"inbox").glob("*.json"):
    try:
        d=json.loads(f.read_text())
        # אם זה result חדש
        if "cleaned_opportunity" in d:
            s=d["cleaned_opportunity"]["signal"]
            s=re.sub(r'to the referral.*?\}\},','', s)
            s="Platform Referr allows selling leads, Stripe payout minus 3% fee (min £3)"
            d["cleaned_opportunity"]["signal"]=s
            f.write_text(json.dumps(d, indent=2, ensure_ascii=False))
    except: pass
print("cleaned inbox")
