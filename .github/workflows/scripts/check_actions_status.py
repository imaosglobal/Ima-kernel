#!/usr/bin/env python3
import json, os, time
import requests

repo=os.environ["GITHUB_REPOSITORY"]
token=os.environ["GITHUB_TOKEN"]
with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as f: event=json.load(f)
sha=event.get("pull_request",{}).get("head",{}).get("sha") or os.environ.get("GITHUB_SHA")
headers={"Accept":"application/vnd.github+json","Authorization":f"Bearer {token}"}
url=f"https://api.github.com/repos/{repo}/commits/{sha}/check-runs?per_page=100"
deadline=time.time()+180
while True:
    rs=requests.get(url,headers=headers,timeout=20); rs.raise_for_status()
    runs=[r for r in rs.json().get("check_runs",[]) if r.get("name")!="Check PR Status"]
    pending=[r for r in runs if r.get("status")!="completed"]
    bad=[r for r in runs if r.get("status")=="completed" and r.get("conclusion") not in {"success","neutral","skipped"}]
    if bad:
        print("FAILED CHECKS:")
        for r in bad: print(f"- {r.get('name')}: {r.get('conclusion')}")
        raise SystemExit(1)
    if not pending: print(f"PR checks clean: {len(runs)} completed check(s)"); raise SystemExit(0)
    if time.time()>=deadline: print("Timed out waiting for PR checks"); raise SystemExit(1)
    print(f"Waiting for {len(pending)} check(s)..."); time.sleep(15)
