import subprocess
from .base import Provider

class GitProvider(Provider):
    def get_diff(self):
        try:
            result = subprocess.run(["git", "diff", "HEAD"], capture_output=True, text=True)
            return result.stdout
        except:
            return ""
    def get_name(self): return "git"
