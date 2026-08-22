import subprocess
import sys
from reasoning_layer import interpret
from answer_builder import build_answer
from providers.git import GitProvider
from providers.github import GitHubProvider
from providers.gitlab import GitLabProvider

def get_provider():
    try:
        remotes = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True).stdout
        if "github" in remotes: return GitHubProvider()
        if "gitlab" in remotes: return GitLabProvider()
    except: pass
    return GitProvider()

class IMAReviewer:
    def __init__(self):
        self.provider = get_provider()

    def run(self):
        diff = self.provider.get_diff()
        result = interpret(diff)
        message, recovery = build_answer(result)
        self.print_report(result['score'], message, recovery)
        self.check_commit_msg()

    def print_report(self, score, message, recovery):
        for i, step in enumerate(recovery, 1):

    def check_commit_msg(self):

def run_lint():
    commands = ["black.", "flake8. --ignore=E501", "isort."]
    for cmd in commands:
        subprocess.run(cmd, shell=True, capture_output=True)

def generate_commit_msg(diff):
    diff_lower = diff.lower()
    if "fix" in diff_lower or "bug" in diff_lower: return "fix: תיקון באג"
    elif "add" in diff_lower or "new" in diff_lower: return "feat: הוספת פיצ'ר חדש"
    elif "refactor" in diff_lower: return "refactor: ריפקטור קוד"
    else: return "chore: עדכון כללי"

def generate_fix(diff):
    fixes = []
    if "TODO" in diff: fixes.append("echo 'יש TODO לטפל לפני merge'")
    if not fixes: fixes.append("echo 'אין תיקונים אוטומטיים'")
    return fixes

def generate_explain(diff):
    elif "def " in diff: return "ה-PR הזה מוסיף פונקציות חדשות"
    else: return "ה-PR הזה מבצע עדכון כללי"

def ship_code(provider):
    run_lint()

    diff = provider.get_diff()
    fixes = generate_fix(diff)
    for f in fixes:
        subprocess.run(f, shell=True)

    msg = generate_commit_msg(diff)
    subprocess.run(["git", "add", "."], capture_output=True)
    subprocess.run(["git", "commit", "-m", msg], capture_output=True)

    subprocess.run(["git", "push"], capture_output=True)

    if provider.get_name() == "github":
    elif provider.get_name() == "gitlab":


def main():
    IMAReviewer().run()

if __name__ == "__main__":
    provider = get_provider()
    if len(sys.argv) > 1 and sys.argv[1] == "lint":
        run_lint()
    elif len(sys.argv) > 1 and sys.argv[1] == "commit":
        diff = provider.get_diff()
        msg = generate_commit_msg(diff)
    elif len(sys.argv) > 1 and sys.argv[1] == "fix":
        diff = provider.get_diff()
        fixes = generate_fix(diff)
    elif len(sys.argv) > 1 and sys.argv[1] == "explain":
        diff = provider.get_diff()
        exp = generate_explain(diff)
    elif len(sys.argv) > 1 and sys.argv[1] == "ship":
        ship_code(provider)
    else:
        main()
