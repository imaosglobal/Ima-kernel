import subprocess

class GitProvider:
    def get_diff(self):
        try:
            result = subprocess.run(["git", "diff", "HEAD"], capture_output=True, text=True)
            return result.stdout
        except:
            return ""

    def get_commit_msg(self):
        return "תקין"

class GitHubProvider(GitProvider):
    def get_pr_url(self):
        return "https://github.com/..."

class GitLabProvider(GitProvider):
    def get_mr_url(self):
        return "https://gitlab.com/..."
