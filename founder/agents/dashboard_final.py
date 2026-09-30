#!/usr/bin/env python3
import pathlib, json
BASE = pathlib.Path.home() / "Ima-kernel/.ima"
ALL = BASE / "all_opportunities.jsonl"
print("\n💎 IMA EMPIRE DASHBOARD")
print("="*50)
if ALL.exists():
    for line in ALL.read_text().strip().splitlines():
        try:
            d=json.loads(line)
            opp=d['cleaned_opportunity']
            print(f"✅ {d.get('profit_score')}/100 | {opp['category']:15} | {opp['title'][:40]}")
        except: pass
print("="*50)
print(f"🎯 Mission: Make Ima rich to share worldwide")
print(f"🔒 Safety: consent_required=True")
print(f"🚀 Engine: V4 ALL-OPPORTUNITIES")
import shutil
total, used, free = shutil.disk_usage(str(BASE))
print(f"💾 Free space: {free//1024//1024}MB")
