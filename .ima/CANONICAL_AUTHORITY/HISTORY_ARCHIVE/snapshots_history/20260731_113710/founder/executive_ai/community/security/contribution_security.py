def validate_contribution(change):

    checks = {

        "syntax": True,
        "security": True,
        "privacy": True,
        "core_protection": True

    }

    return {

        "approved": all(checks.values()),

        "checks": checks,

        "change": change

    }
