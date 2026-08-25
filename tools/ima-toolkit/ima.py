import subprocess
import sys

from reasoning_layer import interpret
from answer_builder import build_answer
from providers.git import GitProvider
from providers.github import GitHubProvider
from providers.gitlab import GitLabProvider

VERSION = "4.1.2"


def get_provider():
    try:
        remotes = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True,
            check=False,
        ).stdout.lower()

        if "github" in remotes:
            return GitHubProvider()

        if "gitlab" in remotes:
            return GitLabProvider()

    except Exception:
        pass

    return GitProvider()


class IMAReviewer:
    def __init__(self):
        self.provider = get_provider()

    def run(self):
        print(
            "=== IMA PR REVIEWER v"
            + VERSION
            + " - "
            + self.provider.get_name()
            + " ==="
        )

        diff = self.provider.get_diff()
        result = interpret(diff)
        message, recovery = build_answer(result)

        print("\n" + str(result["score"]) + "/10 - " + message)

        for i, step in enumerate(recovery, 1):
            print(str(i) + ". " + step)


def run_fix():
    print("=== IMA FIX ===")
    print("Fix mode is disabled because the previous implementation modified Python files destructively.")
    print("Use targeted fixes instead.")


def run_test():
    return subprocess.run(
        [
            "pytest",
            "--ignore=_archive_20260808",
            "--ignore=external",
            "-x",
        ],
        check=False,
    ).returncode


def main():
    IMAReviewer().run()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "fix":
        run_fix()
    elif len(sys.argv) > 1 and sys.argv[1] == "test":
        raise SystemExit(run_test())
    else:
        main()
