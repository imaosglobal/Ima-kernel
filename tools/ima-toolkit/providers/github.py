from .git import GitProvider

class GitHubProvider(GitProvider):
    def get_name(self): return "github"
    def get_pr_url(self): return "https://github.com/..."
