"""Evidence-bounded GitHub achievement growth planner for IMA."""
from dataclasses import dataclass, asdict
from typing import List, Dict

@dataclass(frozen=True)
class AchievementOpportunity:
    name: str
    mechanism: str
    legitimate_path: str
    evidence_required: str
    automation_level: str
    priority: int
    status: str = "OPPORTUNITY"

ACHIEVEMENTS = (
    AchievementOpportunity("Pull Shark","merged_pull_requests","Ship real improvements through reviewable pull requests and merge them after QA.","Merged PR events visible to GitHub","AUTOMATABLE_WITH_QA",1),
    AchievementOpportunity("Galaxy Brain","accepted_discussion_answers","Answer real GitHub Discussions questions accurately; have community members accept useful answers.","Accepted answer events","COMMUNITY_REQUIRED",2),
    AchievementOpportunity("Pair Extraordinaire","coauthored_merged_pr","Work with a real collaborator on substantive merged work.","Merged PR with qualifying co-author event","COLLABORATOR_REQUIRED",3),
    AchievementOpportunity("Starstruck","repository_stars","Make the public product genuinely useful, discoverable and shareable so independent users star it.","GitHub star count threshold","COMMUNITY_REQUIRED",4),
    AchievementOpportunity("Quickdraw","rapid_issue_or_pr_close","May occur naturally when a real small issue/PR is resolved rapidly; never create artificial activity solely for the badge.","Qualifying close event","OPPORTUNISTIC_ONLY",5),
    AchievementOpportunity("YOLO","merged_pr_without_review","Only if a legitimate low-risk change qualifies and repository policy permits it; never bypass safety or required review merely for a badge.","Qualifying merge event","HUMAN_POLICY_REQUIRED",6),
    AchievementOpportunity("Public Sponsor","github_sponsorship","Participate in GitHub Sponsors through a real sponsorship transaction, only when independently justified.","Sponsor event","HUMAN_AND_PAYMENT_REQUIRED",7),
)

def build_opportunity_queue(*, verified_events: Dict[str,int]|None=None, repository_health: Dict[str,bool]|None=None)->List[Dict]:
    verified_events=verified_events or {}; repository_health=repository_health or {}
    health_ok=all(repository_health.values()) if repository_health else True
    queue=[]
    for item in ACHIEVEMENTS:
        status="READY" if health_ok and item.automation_level=="AUTOMATABLE_WITH_QA" else item.status
        queue.append({**asdict(item),"verified_evidence_count":int(verified_events.get(item.name,0)),"status":status})
    return sorted(queue,key=lambda x:(x["status"]!="READY",x["priority"]))

def principles():
    return [
        "Earn, never manufacture, achievements.",
        "Prefer useful product/community work that independently benefits IMA.",
        "Never buy/trade stars or solicit fake engagement.",
        "Never expose secrets or private user data.",
        "Never bypass security/review gates solely for a badge.",
        "Separate GitHub platform achievements from real product traction.",
        "Feed achievement lessons into learning, GTM, collaboration and quality loops.",
    ]
