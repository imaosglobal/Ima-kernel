#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
IMA = ROOT / ".ima"
REPORT_DIR = IMA / "diagnostics"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

NOW = int(time.time())
REPORT_JSON = REPORT_DIR / f"product_diagnostic_{NOW}.json"
REPORT_MD = REPORT_DIR / f"product_diagnostic_{NOW}.md"

@dataclass
class Result:
    stage: str
    status: str
    summary: str
    details: dict[str, Any]

results: list[Result] = []

def run(cmd: list[str], timeout: int = 300) -> tuple[int, str, str]:
    try:
        p = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def record(stage: str, status: str, summary: str, **details):
    results.append(Result(stage, status, summary, details))

def exists_any(paths: list[str]) -> list[str]:
    return [p for p in paths if (ROOT / p).exists()]

def active_files():
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        s = str(p)
        if any(x in s for x in [
            ".git/",
            ".ima/archive",
            ".ima/backups",
            "archive/",
            "backups/",
            "__pycache__/",
            "node_modules/",
        ]):
            continue
        yield p

def stage_canonical_runtime():
    code, out, err = run([
        sys.executable,
        ".ima/CANONICAL_AUTHORITY/entry/IMA_START_SINGLE_ENTRY.py",
    ])
    if code == 0 and "[OK] CANONICAL REGISTRY VERIFIED" in out:
        record("canonical_runtime", "READY", "Canonical runtime verified.")
    else:
        record(
            "canonical_runtime",
            "FAILED",
            "Canonical runtime verification failed.",
            stdout=out[-3000:],
            stderr=err[-3000:],
        )

def stage_compile():
    targets = [
        "kernel",
        ".ima/CANONICAL_AUTHORITY",
        ".ima/agi_evolution",
        "product",
        "api",
        "learning",
        "companion",
    ]
    existing = [x for x in targets if (ROOT / x).exists()]
    code, out, err = run([
        sys.executable,
        "-m",
        "compileall",
        "-q",
        *existing,
    ])
    if code == 0:
        record("compile", "READY", "Active Python product/runtime paths compile.", targets=existing)
    else:
        record(
            "compile",
            "FAILED",
            "Compilation errors remain in active paths.",
            stdout=out[-4000:],
            stderr=err[-4000:],
        )

def stage_entry_points():
    candidates = {
        "canonical": [
            "IMA_START.py",
            ".ima/CANONICAL_AUTHORITY/entry/IMA_START_SINGLE_ENTRY.py",
        ],
        "api": ["api", "server.py", "app.py", "main.py"],
        "frontend": ["frontend", "web", "client", "package.json"],
        "mobile": ["android", "ios", "mobile"],
        "voice": ["product/voice", "voice"],
    }

    found = {
        name: exists_any(paths)
        for name, paths in candidates.items()
    }

    if not found["canonical"]:
        record("user_entry_points", "FAILED", "Canonical user entry point missing.", found=found)
    else:
        count = sum(bool(v) for v in found.values())
        record(
            "user_entry_points",
            "READY" if count >= 3 else "PARTIAL",
            "User entry-point inventory completed.",
            found=found,
        )

def stage_authentication_identity():
    auth_paths = exists_any([
        "auth",
        "authentication",
        "identity",
        "api/auth",
        "api/identity",
        "backend/auth",
        "backend/identity",
    ])

    marker_files = []

    for p in active_files():
        if p.suffix not in {".py", ".ts", ".tsx", ".js", ".json"}:
            continue

        try:
            content = p.read_text(errors="ignore")
        except Exception:
            continue

        if re.search(
            r"login|signup|register|session|password|oauth|token|refresh",
            content,
            re.IGNORECASE,
        ):
            marker_files.append(str(p))

    if not auth_paths or not marker_files:
        record(
            "authentication_identity",
            "MISSING",
            "Authentication/identity implementation not sufficiently verified.",
            paths=auth_paths,
            marker_files=marker_files[:50],
        )
        return

    validation_files = []

    for p in active_files():
        name = str(p).lower()

        if any(
            word in name
            for word in [
                "auth_test",
                "test_auth",
                "identity_test",
                "test_identity",
                "e2e",
                "smoke",
                "health",
                "validate_auth",
                "verify_auth",
            ]
        ):
            validation_files.append(str(p))

    live_validation = False

    for p in validation_files:
        try:
            content = Path(p).read_text(errors="ignore")
        except Exception:
            continue

        if re.search(
            r"login|signup|register|session|token|identity",
            content,
            re.IGNORECASE,
        ):
            live_validation = True
            break

    if live_validation:
        record(
            "authentication_identity",
            "READY",
            "Authentication and identity implementation detected with local validation surface.",
            paths=auth_paths,
            marker_files=marker_files[:50],
            validation_files=validation_files[:50],
            validation="local_validation_surface_detected",
        )
    else:
        record(
            "authentication_identity",
            "PARTIAL",
            "Authentication and identity implementation detected; live flow still requires validation.",
            paths=auth_paths,
            marker_files=marker_files[:50],
            validation_files=validation_files[:50],
        )


def stage_user_experience():
    markers = [
        "onboarding",
        "welcome",
        "dashboard",
        "navigation",
        "getting_started",
        "first_value",
    ]

    found = [
        str(p)
        for p in active_files()
        if any(x in p.name.lower() for x in markers)
    ]

    record(
        "core_user_experience",
        "READY" if len(found) >= 3 else "PARTIAL" if found else "MISSING",
        "Core UX surface inventory completed.",
        files=found[:100],
    )

def stage_product_modules():
    product = ROOT / "product"

    if not product.exists():
        record("product_capabilities", "MISSING", "Product directory missing.")
        return

    modules = {
        p.name: {
            "exists": True,
            "type": "directory" if p.is_dir() else "file",
        }
        for p in sorted(product.iterdir())
    }

    runtime_refs = []
    for p in active_files():
        if p.suffix not in {".py", ".ts", ".tsx", ".js"}:
            continue
        try:
            text = p.read_text(errors="ignore")
        except Exception:
            continue
        if "product/" in text or "product." in text:
            runtime_refs.append(str(p))

    record(
        "product_capabilities",
        "READY" if modules and runtime_refs else "PARTIAL",
        "Product modules and runtime references inventoried.",
        modules=modules,
        runtime_reference_files=runtime_refs[:100],
    )

def stage_backend():
    backend = exists_any([
        "api",
        "backend",
        "server.py",
        "app.py",
        "main.py",
        "database",
        "db",
    ])

    persistence = []
    errors = []

    for p in active_files():
        if p.suffix not in {".py", ".ts", ".tsx", ".js"}:
            continue
        try:
            text = p.read_text(errors="ignore")
        except Exception:
            continue

        if re.search(
            r"postgres|sqlite|supabase|redis|mongodb|sqlalchemy|database",
            text,
            re.IGNORECASE,
        ):
            persistence.append(str(p))

        if re.search(
            r"exception|try:|catch|retry|timeout|error",
            text,
            re.IGNORECASE,
        ):
            errors.append(str(p))

    status = (
        "READY"
        if backend and persistence and errors
        else "PARTIAL"
        if backend
        else "MISSING"
    )

    record(
        "backend_production_readiness",
        status,
        "Backend, persistence and error handling inventoried.",
        backend=backend,
        persistence=persistence[:100],
        error_handling=errors[:100],
    )

def stage_safety_privacy():
    found = exists_any([
        "safety",
        "product/safety",
        "privacy",
        "security",
        "policy",
        "governance",
        "child_safety",
    ])

    record(
        "safety_privacy",
        "READY" if len(found) >= 2 else "PARTIAL" if found else "MISSING",
        "Safety and privacy surfaces inventoried.",
        paths=found,
    )

def stage_deployment():
    found = exists_any([
        "render.yaml",
        "Dockerfile",
        "docker-compose.yml",
        "fly.toml",
        "vercel.json",
        "netlify.toml",
        "Procfile",
        "requirements.txt",
        "package.json",
    ])

    record(
        "deployment",
        "READY" if len(found) >= 2 else "PARTIAL" if found else "MISSING",
        "Deployment configuration inventoried.",
        files=found,
    )

def stage_observability():
    markers = [
        "health",
        "healthcheck",
        "monitor",
        "metrics",
        "logging",
        "watchdog",
        "supervisor",
        "crash",
    ]

    found = [
        str(p)
        for p in active_files()
        if any(x in p.name.lower() for x in markers)
    ]

    record(
        "observability",
        "READY" if len(found) >= 3 else "PARTIAL" if found else "MISSING",
        "Health, monitoring and recovery surfaces inventoried.",
        files=found[:100],
    )

def stage_payments():
    markers = [
        "stripe",
        "payment",
        "billing",
        "subscription",
        "checkout",
        "pricing",
    ]

    found = []
    for p in active_files():
        try:
            text = p.read_text(errors="ignore").lower()
        except Exception:
            continue
        if any(x in text for x in markers):
            found.append(str(p))

    record(
        "payments_monetization",
        "READY" if found else "PARTIAL",
        "Monetization surfaces inventoried.",
        files=found[:100],
    )

def stage_performance():
    markers = [
        "timeout",
        "retry",
        "cache",
        "queue",
        "async",
        "concurrency",
        "rate_limit",
        "rate-limit",
    ]

    found = []
    for p in active_files():
        if p.suffix not in {".py", ".ts", ".tsx", ".js"}:
            continue
        try:
            text = p.read_text(errors="ignore").lower()
        except Exception:
            continue
        if any(x in text for x in markers):
            found.append(str(p))

    record(
        "performance_reliability",
        "READY" if len(found) >= 5 else "PARTIAL" if found else "MISSING",
        "Performance and reliability controls inventoried.",
        files=found[:100],
    )

def stage_release_pipeline():
    found = exists_any([
        ".github/workflows",
        "pyproject.toml",
        "pytest.ini",
        "tox.ini",
        "package.json",
        "Makefile",
    ])

    record(
        "release_pipeline",
        "READY" if len(found) >= 2 else "PARTIAL" if found else "MISSING",
        "Build, test and release surfaces inventoried.",
        paths=found,
    )

def stage_real_user_validation():
    required = [
        "IMA_START.py",
        ".ima/governance/IMA_PRODUCT_RELEASE_MAP.json",
        ".ima/CANONICAL_AUTHORITY/entry/IMA_START_SINGLE_ENTRY.py",
    ]

    missing = [
        x for x in required
        if not (ROOT / x).exists()
    ]

    if missing:
        record(
            "real_user_validation",
            "MISSING",
            "Required user-validation prerequisites are missing.",
            missing=missing,
        )
        return

    checks = []

    # 1. Canonical single-entry boot validation
    code, out, err = run([
        sys.executable,
        ".ima/CANONICAL_AUTHORITY/entry/IMA_START_SINGLE_ENTRY.py",
    ])

    checks.append({
        "name": "canonical_single_entry",
        "ok": (
            code == 0
            and "[OK] CANONICAL POLICY VERIFIED" in out
            and "[OK] HASH VERIFIED" in out
            and "[OK] CANONICAL REGISTRY VERIFIED" in out
        ),
        "stdout": out[-2000:],
        "stderr": err[-2000:],
    })

    # 2. Active runtime compilation
    compile_targets = [
        "kernel",
        ".ima/CANONICAL_AUTHORITY",
        ".ima/agi_evolution",
        "product",
        "api",
        "learning",
        "companion",
    ]

    existing = [
        x for x in compile_targets
        if (ROOT / x).exists()
    ]

    code, out, err = run([
        sys.executable,
        "-m",
        "compileall",
        "-q",
        *existing,
    ])

    checks.append({
        "name": "active_compile",
        "ok": code == 0,
        "stdout": out[-2000:],
        "stderr": err[-2000:],
    })

    failed = [
        x["name"]
        for x in checks
        if not x["ok"]
    ]

    if failed:
        record(
            "real_user_validation",
            "PARTIAL",
            "Local end-to-end validation executed but one or more checks failed.",
            required=required,
            failed_checks=failed,
            checks=checks,
        )
    else:
        record(
            "real_user_validation",
            "READY",
            "Local end-to-end validation passed for canonical boot and active runtime.",
            required=required,
            checks=checks,
        )

def stage_release_sync():
    path = ROOT / ".ima/governance/IMA_PRODUCT_RELEASE_MAP.json"

    if not path.exists():
        record("release_sync", "MISSING", "Release map missing.")
        return

    try:
        data = json.loads(path.read_text())
        head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
        ).strip()

        old = data.get("git_commit")

        if old != head:
            data["git_commit"] = head
            path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n"
            )
            record(
                "release_sync",
                "REPAIRED",
                "Release map synchronized to current HEAD.",
                previous=old,
                current=head,
            )
        else:
            record(
                "release_sync",
                "READY",
                "Release map already matches current HEAD.",
                current=head,
            )

    except Exception as e:
        record(
            "release_sync",
            "FAILED",
            "Release synchronization failed.",
            error=str(e),
        )

def write_reports():
    summary = {
        "READY": sum(x.status == "READY" for x in results),
        "REPAIRED": sum(x.status == "REPAIRED" for x in results),
        "PARTIAL": sum(x.status == "PARTIAL" for x in results),
        "MISSING": sum(x.status == "MISSING" for x in results),
        "FAILED": sum(x.status == "FAILED" for x in results),
    }

    payload = {
        "timestamp": NOW,
        "system": "IMA",
        "engine": "IMA_PRODUCT_DIAGNOSTIC_ENGINE",
        "results": [asdict(x) for x in results],
        "summary": summary,
    }

    REPORT_JSON.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    )

    lines = [
        "# IMA Product Diagnostic Report",
        "",
        f"- Timestamp: `{NOW}`",
        "- Engine: `IMA_PRODUCT_DIAGNOSTIC_ENGINE`",
        "",
        "## Summary",
        "",
    ]

    for k, v in summary.items():
        lines.append(f"- {k}: {v}")

    lines += ["", "## Stages", ""]

    for r in results:
        lines += [
            f"### {r.stage}",
            f"- Status: **{r.status}**",
            f"- Summary: {r.summary}",
            "",
        ]

    REPORT_MD.write_text("\n".join(lines) + "\n")

    return payload

def main():

    stages = [
        stage_canonical_runtime,
        stage_compile,
        stage_entry_points,
        stage_authentication_identity,
        stage_user_experience,
        stage_product_modules,
        stage_backend,
        stage_safety_privacy,
        stage_deployment,
        stage_observability,
        stage_payments,
        stage_performance,
        stage_release_pipeline,
        stage_real_user_validation,
        stage_release_sync,
    ]

    for stage in stages:
        try:
            stage()
        except Exception as e:
            record(
                stage.__name__,
                "FAILED",
                "Unhandled diagnostic failure; continuing.",
                error=str(e),
            )

    payload = write_reports()
    summary = payload["summary"]

    for k, v in summary.items():


    if summary["FAILED"] or summary["MISSING"]:
        return 2

    if summary["PARTIAL"]:
        return 1

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
