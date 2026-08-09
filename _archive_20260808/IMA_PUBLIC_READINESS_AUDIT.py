from pathlib import Path
import json

ROOT = Path(".")
IMA = ROOT / ".ima"

checks = {}

# Product layer
checks["product_layer"] = any(
    p.exists()
    for p in [
        ROOT / "product",
        ROOT / "app",
        ROOT / "web",
        ROOT / "frontend",
        ROOT / "public"
    ]
)

# Server/API
checks["server"] = any(
    p.exists()
    for p in [
        ROOT / "server.py",
        ROOT / "api",
        ROOT / "backend",
        ROOT / "server",
        ROOT / "docker-compose.yml"
    ]
)

# Domain / public endpoint indicators
checks["domain_config"] = any(
    p.exists()
    for p in [
        ROOT / ".env",
        ROOT / "domain.json",
        ROOT / "deployment.json",
        ROOT / "vercel.json",
        ROOT / "netlify.toml"
    ]
)

# Application/interface
checks["interface"] = any(
    p.exists()
    for p in [
        ROOT / "frontend",
        ROOT / "ui",
        ROOT / "templates",
        ROOT / "static",
        ROOT / "app"
    ]
)

# User system
checks["user_system"] = any(
    p.exists()
    for p in [
        ROOT / "users",
        ROOT / "auth",
        ROOT / "database",
        ROOT / "supabase",
        ROOT / "accounts"
    ]
)

# Usage telemetry
checks["usage_loop"] = any(
    p.exists()
    for p in [
        ROOT / "analytics",
        ROOT / "telemetry",
        ROOT / "metrics",
        ROOT / "events"
    ]
)

# Distribution
checks["distribution"] = any(
    p.exists()
    for p in [
        ROOT / "marketing",
        ROOT / "landing",
        ROOT / "social",
        ROOT / "integrations"
    ]
)

# Existing core
checks["core"] = (IMA / "CANONICAL_AUTHORITY").exists()
checks["management"] = (IMA / "MANAGEMENT").exists()
checks["git"] = (ROOT / ".git").exists()


print("=== IMA PUBLIC READINESS AUDIT ===")
print()

for k,v in checks.items():
    print(("[OK] " if v else "[MISSING] "), k)

missing = [
    k for k,v in checks.items()
    if not v
]

report = {
    "status": "READY_FOR_PRODUCT" if not missing else "INFRA_ONLY",
    "missing": missing,
    "checks": checks
}

out = IMA / "MANAGEMENT/public_readiness_audit.json"
out.write_text(json.dumps(report, indent=2))

print()
print("STATUS:", report["status"])
print("REPORT:", out)

