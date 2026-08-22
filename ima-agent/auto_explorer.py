import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
import sys
import requests

ENV_FILE = Path.home() / "ima_kernel" / ".env"
TOKEN = ""
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        if line.startswith("GH_TOKEN="):
            TOKEN = line.split("=", 1)[1].strip()

HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}
WATCHLIST = ["facebook/react", "pytorch/pytorch", "imaosglobal/Ima-kernel"]


def log(msg):
    print(msg, flush=True)
    with open(os.path.expanduser("~/ima_agent.log"), "a") as f:
        f.write(f"{datetime.now()} {msg}\n")


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def hunt_issues():
    log("[IMA HUNT] Scanning watchlist for good issues...")
    for repo in WATCHLIST:
        url = f"https://api.github.com/repos/{repo}/issues"
        params = {"state": "open", "labels": "good first issue,bug,help wanted", "per_page": 5}
        r = requests.get(url, headers=HEADERS, params=params)
        if r.status_code == 200:
            for issue in r.json():
                if "pull_request" not in issue:
                    log(f"[FOUND] {repo} | #{issue['number']} | {issue['title']}\nURL: {issue['html_url']}")
        else:
            log(f"[IMA HUNT] {repo}: HTTP {r.status_code}")


def draft_pr(repo_path):
    log(f"[IMA PR] Analyzing staged changes in {repo_path}")
    diff = run(["git", "-C", repo_path, "diff", "--cached"]).stdout
    if not diff:
        log("No staged changes. Run 'git add' first.")
        return

    title = "fix: improve error handling and logging"
    body = (
        "## What\n"
        "Suggested draft by IMA dev tools (review before submitting)\n\n"
        "## Changes\n"
        "- (fill in what you actually changed)\n\n"
        "## Diff summary\n"
        "```diff\n" + diff[:800] + "\n```"
    )
    log(f"[IMA PR] Suggested Title: {title}")
    log(f"[IMA PR] Suggested Body:\n{body}")
    log("Review and edit, then run: gh pr create -t '...' -b '...'")


def cto_review(path):
    log(f"[IMA CTO] Reviewing {path}")
    py_files = list(Path(path).expanduser().rglob("*.py"))
    for f in py_files[:10]:
        code = f.read_text(errors="ignore")
        issues = []
        if "print(" in code:
            issues.append("Consider using logging instead of print")
        if "except:" in code:
            issues.append("Use 'except Exception as e:' instead of bare except")
        if "def " in code and "->" not in code:
            issues.append("Some functions may be missing type hints")
        if issues:
            log(f"\n[FILE] {f.name}")
            for i in issues:
                log(f" - {i}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "hunt":
        hunt_issues()
    elif cmd == "pr":
        draft_pr(sys.argv[2] if len(sys.argv) > 2 else ".")
    elif cmd == "cto":
        cto_review(sys.argv[2] if len(sys.argv) > 2 else "~/ima_kernel")
    else:
        print("Usage: python auto_explorer.py [hunt|pr|cto]")
