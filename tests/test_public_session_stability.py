import ast
from pathlib import Path


APP = Path(__file__).resolve().parents[1] / "app.py"


def _source():
    return APP.read_text(encoding="utf-8")


def test_session_secret_has_no_per_process_random_fallback():
    source = _source()
    tree = ast.parse(source)
    assignments = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "SESSION_SECRET":
                    assignments.append(node)

    assert len(assignments) == 1
    assignment = assignments[0]
    rendered = ast.unparse(assignment.value)
    assert "secrets.token_hex" not in rendered
    assert "IMA_SESSION_SECRET" in rendered


def test_session_secret_fails_closed_when_missing():
    source = _source()
    assert 'raise RuntimeError("IMA_SESSION_SECRET must be configured; refusing to start with a per-process session secret")' in source


def test_flask_secret_does_not_have_an_independent_random_fallback():
    source = _source()
    assert 'app.config["SECRET_KEY"] = os.environ.get("IMA_FLASK_SECRET") or os.environ.get("IMA_SESSION_SECRET") or secrets.token_hex(32)' not in source
