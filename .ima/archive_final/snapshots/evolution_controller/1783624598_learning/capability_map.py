from pathlib import Path
import ast
import json


OUTPUT = Path("learning/capability_map.json")


def build_capability_map():

    data = {}

    for file in Path("learning").glob("*.py"):

        try:
            tree = ast.parse(file.read_text(encoding="utf-8"))

            functions = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)

            data[file.stem] = {
                "functions": functions
            }

        except Exception:
            pass

    OUTPUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    return data
