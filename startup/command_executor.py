import subprocess
from pathlib import Path

class CommandExecutor:

    ALLOWED = [
        "cat ",
        "ls",
        "find",
        "pwd",
        "git status",
        "git log",
        "git remote",
        "du ",
        "wc ",
    ]

    def classify(self, command):
        if command.startswith("cat "):
            return "file_read"
        if command.startswith("git"):
            return "git"
        if command.startswith("ls") or command.startswith("find"):
            return "filesystem"
        return "system"

    def run(self, command):
        command = command.strip()

        if not any(command.startswith(x) for x in self.ALLOWED):
            return f"פקודה לא מאושרת: {command}"

        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=Path("."),
                capture_output=True,
                text=True,
                timeout=15
            )

            output = result.stdout if result.stdout else result.stderr

            return (
                f"[IMA Command Result]\n"
                f"Type: {self.classify(command)}\n"
                f"Command: {command}\n\n"
                f"{output[:4000]}"
            )

        except Exception as e:
            return f"שגיאת ביצוע: {e}"
