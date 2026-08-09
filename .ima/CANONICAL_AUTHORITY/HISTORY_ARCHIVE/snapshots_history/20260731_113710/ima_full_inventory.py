from pathlib import Path
import json
import os


ROOT = Path(".")


EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "react",
    ".ts": "typescript",
    ".tsx": "react_typescript",
    ".json": "json",
    ".md": "documentation",
    ".yml": "config",
    ".yaml": "config",
    ".sh": "shell",
    ".gradle": "android_build",
    ".xml": "android",
    ".html": "web",
    ".css": "style"
}


def scan():

    result = {
        "files": [],
        "folders": [],
        "technologies": {},
        "important_files": []
    }

    for p in ROOT.rglob("*"):

        if any(x in str(p) for x in [
            "node_modules",
            ".git/objects",
            "__pycache__"
        ]):
            continue

        if p.is_dir():
            result["folders"].append(str(p))
            continue

        ext = p.suffix.lower()

        tech = EXTENSIONS.get(ext)

        if tech:
            result["technologies"][tech] = (
                result["technologies"].get(tech, 0) + 1
            )

        item = {
            "path": str(p),
            "size": p.stat().st_size,
            "type": tech or "unknown"
        }

        result["files"].append(item)


        name = p.name.lower()

        if any(x in name for x in [
            "package.json",
            "readme",
            "docker",
            "dockerfile",
            "requirements",
            "android",
            "manifest",
            "git",
            "next",
            "vite",
            "react",
            "server",
            "api",
            "model",
            ".env"
        ]):
            result["important_files"].append(str(p))


    return result


data = scan()


Path("ima_full_inventory.json").write_text(
    json.dumps(
        data,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)


print("=== IMA FULL INVENTORY ===")
print("FILES:", len(data["files"]))
print("FOLDERS:", len(data["folders"]))

print("\nTECHNOLOGIES:")
for k,v in data["technologies"].items():
    print(k, ":", v)

print("\nIMPORTANT FILES:")
for x in data["important_files"][:100]:
    print("-", x)

print("\nCREATED ima_full_inventory.json")
