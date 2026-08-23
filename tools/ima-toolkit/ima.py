import subprocess
import sys
import os
import glob
import time
import shutil
import importlib.util
from datetime import datetime
from reasoning_layer import interpret
from answer_builder import build_answer
from providers.git import GitProvider
from providers.github import GitHubProvider
from providers.gitlab import GitLabProvider

VERSION = "4.0.1"
NOTE_FILE = os.path.expanduser("~/.ima_notes")
PLUGIN_DIR = os.path.expanduser("~/.ima_plugins")

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

def run_help():
    cmds = {
        "קוד": ["pr-review", "lint", "test", "ship", "commit", "fix", "explain", "ai-review"],
        "מעקב": ["stats", "todo", "watch", "search"],
        "ניקוי": ["clean"],
        "DevOps": ["docker", "deploy", "backup", "db", "serve"],
        "פרודוקטיביות": ["note", "time", "env"],
        "מערכת": ["plugin", "help", "version"]
    }
    for cat, items in cmds.items():

def run_version():

def run_lint():
    for cmd in ["black.", "flake8. --ignore=E501", "isort."]:

def run_test():
    result = subprocess.run("pytest --cov --cov-report=term-missing 2>/dev/null || echo 'התקן: pip install pytest-cov'", shell=True)

def run_stats():
    files = len([f for f in glob.glob("**/*.*", recursive=True) if ".git" not in f and "node_modules" not in f])
    lines = subprocess.run("find. -type f -name '*.py' -o -name '*.ts' -o -name '*.js' | xargs wc -l 2>/dev/null | tail -1", shell=True, capture_output=True, text=True).stdout
    commits = subprocess.run("git rev-list --count HEAD 2>/dev/null", shell=True, capture_output=True, text=True).stdout

def run_todo():
    result = subprocess.run("grep -rn '# TODO'. --exclude-dir=.git --exclude-dir=node_modules", shell=True, capture_output=True, text=True)

def run_clean():
    for pattern in ["**/__pycache__", "**/*.pyc", "**/.pytest_cache", "dist", "build", "node_modules"]:
        for p in glob.glob(pattern, recursive=True): subprocess.run(f"rm -rf '{p}'", shell=True)

def run_watch():
    last = 0
    while True:
        current = sum(os.path.getmtime(f) for f in glob.glob("**/*.*", recursive=True) if ".git" not in f)
        if current!= last:
            run_lint(); run_test(); last = current
        time.sleep(2)

def run_docker():
    subprocess.run("docker build -t ima-app.", shell=True)
    subprocess.run("docker run -p 8000:8000 ima-app", shell=True)

def run_deploy():
    user = input("שרת user@host: ")
    subprocess.run(f"rsync -av --exclude=.git. {user}:~/app/", shell=True)
    subprocess.run(f"ssh {user} 'cd ~/app && docker compose up -d --build'", shell=True)

def run_backup():
    dest = os.path.expanduser("~/ima_backup")
    os.makedirs(dest, exist_ok=True)
    folder = os.path.basename(os.getcwd())
    zip_name = f"{dest}/{folder}_{datetime.now().strftime('%Y%m%d_%H%M')}.tar.gz"
    subprocess.run(f"tar -czf {zip_name}. --exclude=.git --exclude=__pycache__ --exclude=node_modules", shell=True)

def run_db():
    action = input("backup/restore: ")
    db = input("שם DB: ")
    if action == "backup":
        subprocess.run(f"pg_dump {db} > {db}_{datetime.now().strftime('%Y%m%d')}.sql", shell=True)
    elif action == "restore":
        file = input("קובץ sql: ")
        subprocess.run(f"psql {db} < {file}", shell=True)

def run_serve():
    if os.path.exists("app.py") or os.path.exists("main.py"):
        subprocess.run("uvicorn main:app --reload --port 8000", shell=True)
    else:
        subprocess.run("python -m http.server 8000", shell=True)

def run_note(arg):
    if not arg:
        return
    with open(NOTE_FILE, "a") as f: f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {arg}\n")

def run_time(minutes=25):
    for i in range(int(minutes)*60, 0, -1):

def run_search(keyword):
    subprocess.run(f"grep -rn '{keyword}'. --exclude-dir=.git --exclude-dir=node_modules", shell=True)

def run_env():
    if not os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key = line.split("=")[0]

def run_plugin(arg):
    os.makedirs(PLUGIN_DIR, exist_ok=True)
    if arg == "list":
    else:

def generate_commit_msg(diff):
    d = diff.lower()
    if "fix" in d or "bug" in d: return "fix: תיקון באג"
    elif "add" in d or "new" in d: return "feat: הוספת פיצ'ר חדש"
    elif "refactor" in d: return "refactor: ריפקטור קוד"
    else: return "chore: עדכון כללי"

def generate_fix(diff):
    fixes = []
    if "TODO" in diff: fixes.append("echo 'יש TODO לטפל לפני merge'")
    if not fixes: fixes.append("echo 'אין תיקונים אוטומטיים'")
    return fixes

def generate_explain(diff):
    d = diff.lower()
    if "fork" in d and "opensession" in d: return "מבצע fork ל-session נוכחי ומוסיף sessionTypeSelectionReason"
    elif "sessiontypeselectionreason" in d: return "מוסיף מטא-דאטה ל-openSession לצורך מעקב"
    elif "def " in d: return "מוסיף פונקציות חדשות"
    elif "import " in d: return "מוסיף תלויות חדשות"
    else: return "עדכון כללי"

def ai_review(provider):

def ship_code(provider):
    run_lint(); run_test(); ai_review(provider)
    diff = provider.get_diff(); fixes = generate_fix(diff)
    msg = generate_commit_msg(diff)
    subprocess.run(["git", "add", "."], capture_output=True)
    subprocess.run(["git", "commit", "-m", msg], capture_output=True)
    subprocess.run(["git", "push"], capture_output=True)

def load_plugins():
    if not os.path.exists(PLUGIN_DIR): return {}
    plugins = {}
    for f in os.listdir(PLUGIN_DIR):
        if f.endswith(".py"):
            name = f[:-3]
    return plugins

def main():
    IMAReviewer().run()

if __name__ == "__main__":
    provider = get_provider()
    arg = sys.argv[2] if len(sys.argv) > 2 else ""
    plugins = load_plugins()
    cmds = {
        "help": run_help, "version": run_version, "lint": run_lint, "test": run_test, "stats": run_stats,
        "todo": run_todo, "clean": run_clean, "watch": run_watch, "docker": run_docker, "deploy": run_deploy,
        "backup": run_backup, "db": run_db, "serve": run_serve, "note": lambda: run_note(arg),
        "time": lambda: run_time(arg if arg else 25), "search": lambda: run_search(arg), "env": run_env,
        "plugin": lambda: run_plugin(arg), "ai-review": ai_review,
        "ship": lambda: ship_code(provider)
    }
    cmds.update(plugins)
    if len(sys.argv) > 1 and sys.argv[1] in cmds: cmds[sys.argv[1]]()
    else: main()
