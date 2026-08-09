from pathlib import Path
import ast


def scan_system():

    root = Path(".")
    modules = []
    imports = []

    for file in root.rglob("*.py"):

        if "__pycache__" in str(file):
            continue

        try:
            tree = ast.parse(file.read_text(encoding="utf-8"))

            module = str(file)

            modules.append(module)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for item in node.names:
                        imports.append({
                            "file": module,
                            "import": item.name
                        })

                if isinstance(node, ast.ImportFrom):
                    imports.append({
                        "file": module,
                        "import": node.module
                    })

        except Exception:
            pass

    return {
        "modules": modules,
        "imports": imports,
        "module_count": len(modules),
        "import_count": len(imports)
    }


def suggest_improvements():

    scan = scan_system()
    suggestions = []

    learning_files = [
        x for x in scan["modules"]
        if "learning" in x
    ]

    if len(learning_files) > 0:
        suggestions.append(
            "לחבר את כל מנועי learning דרך נקודת orchestrator אחת"
        )

    if scan["import_count"] > scan["module_count"] * 3:
        suggestions.append(
            "לבדוק תלות גבוהה בין מודולים ולשפר הפרדת שכבות"
        )

    suggestions.extend([
        "להוסיף מפת יכולות דינמית של IMA",
        "להוסיף בדיקות בריאות לכל מנוע לפני הפעלה",
        "להוסיף מערכת דירוג איכות לכל מחזור למידה",
        "להוסיף מנגנון מניעת כפילויות ידע ולמידה"
    ])

    return {
        "system_scan": scan,
        "suggestions": suggestions
    }
