import json
from pathlib import Path
from learning.github_achievement_growth import build_opportunity_queue,principles
out=Path("artifacts/web-intelligence/daily-github-achievement-growth.json")
out.parent.mkdir(parents=True,exist_ok=True)
q=build_opportunity_queue(repository_health={"qa":True,"deploy":True})
out.write_text(json.dumps({"schema_version":"1.0","system":"IMA","mode":"evidence_bounded","opportunities":q,"principles":principles(),"next_action":q[0] if q else None},ensure_ascii=False,indent=2),encoding="utf-8")
print("IMA_GITHUB_ACHIEVEMENT_SCAN=RECORDED")
print("TOP_OPPORTUNITY=",q[0]["name"] if q else "NONE")
