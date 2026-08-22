from.git import GitProvider

class GitLabProvider(GitProvider):
    def get_name(self): return "gitlab"
    def get_mr_url(self): return "https://gitlab.com/..."
