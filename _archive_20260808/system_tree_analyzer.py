from pathlib import Path
import ast
import json


ROOT = Path(".")


def scan_files():
    files = []

    for p in ROOT.rglob("*.py"):
        if "backup" in str(p):
            continue

        files.append(p)

    return files


def analyze_file(path):
    result = {
        "file": str(path),
        "imports": [],
        "functions": [],
        "classes": []
    }

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):
                for item in node.names:
                    result["imports"].append(item.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    result["imports"].append(node.module)

            elif isinstance(node, ast.FunctionDef):
                result["functions"].append(node.name)

            elif isinstance(node, ast.ClassDef):
                result["classes"].append(node.name)

    except Exception as e:
        result["error"] = str(e)

    return result


def build_graph(data):

    graph = {}

    for item in data:
        graph[item["file"]] = {
            "imports": item["imports"]
        }

    return graph


def main():

    files = scan_files()

    report = [
        analyze_file(f)
        for f in files
    ]

    graph = build_graph(report)

    output = {
        "total_files": len(files),
        "files": report,
        "dependency_graph": graph
    }

    Path("ima_system_map.json").write_text(
        json.dumps(
            output,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print("=== IMA SYSTEM TREE ANALYSIS ===")
    print("PYTHON FILES:", len(files))

    imports = sum(
        len(x["imports"])
        for x in report
    )

    functions = sum(
        len(x["functions"])
        for x in report
    )

    print("IMPORT LINKS:", imports)
    print("FUNCTIONS:", functions)
    print()
    print("CREATED: ima_system_map.json")


if __name__ == "__main__":
    main()
