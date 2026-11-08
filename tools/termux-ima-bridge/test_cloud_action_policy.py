#!/usr/bin/env python3
"""Regression test for the Termux/Chrome cloud-command security boundary.

This test intentionally uses only Python's standard library. It validates that
cloud-issued actions cannot reach arbitrary JavaScript evaluation.
"""
from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "bridge.py"
TREE = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))


def find_function(name):
    return next(
        node for node in TREE.body
        if isinstance(node, ast.FunctionDef) and node.name == name
    )


def test_cloud_allowlist_excludes_eval():
    assignment = next(
        node for node in TREE.body
        if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "CLOUD_ALLOWED_ACTIONS"
                for t in node.targets)
    )
    value = ast.literal_eval(assignment.value)
    assert "eval" not in value
    assert {"status", "tabs", "screenshot", "navigate", "click", "tap",
            "scroll", "type", "key"} <= value


def test_cloud_gate_rejects_before_dispatch():
    fn = find_function("execute_cloud_action")
    source = ast.get_source_segment(SOURCE.read_text(encoding="utf-8"), fn) or ""
    assert "if action not in CLOUD_ALLOWED_ACTIONS" in source
    assert "cloud_action_not_allowed" in source
    assert "return execute_action(action, payload)" in source


if __name__ == "__main__":
    test_cloud_allowlist_excludes_eval()
    test_cloud_gate_rejects_before_dispatch()
    print("TERMUX_CLOUD_ACTION_SECURITY=PASS")
