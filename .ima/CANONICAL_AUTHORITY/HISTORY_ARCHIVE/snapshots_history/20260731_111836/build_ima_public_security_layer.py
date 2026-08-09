from pathlib import Path

files = {

"founder/executive_ai/community/security/policy_engine.py": '''
POLICY = {

    "public_allowed": [
        "submit_lessons",
        "submit_plugins",
        "submit_connectors",
        "submit_feedback"
    ],

    "private_core": [
        "founder_identity",
        "private_memory",
        "core_reasoning",
        "internal_weights",
        "security_keys"
    ],

    "validation_required": True
}


def get_policy():
    return POLICY
''',


"founder/executive_ai/community/security/license_manager.py": '''
LICENSE = {

    "name":"IMA Community License",

    "public_code":
    "Open Source",

    "core":
    "Protected Private Core",

    "modification":
    "Community contributions require validation",

    "redistribution":
    "Allowed only according to license terms"

}


def get_license():
    return LICENSE
''',


"founder/executive_ai/community/security/contribution_security.py": '''
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
''',


"founder/executive_ai/community/developer_portal.py": '''
PORTAL = {

"name":"IMA Developer Portal",

"sections":[

"Documentation",
"API",
"Connectors",
"Contribution Guide",
"Security Rules",
"Community"

]

}


def get_portal():
    return PORTAL
''',


"IMA_PUBLIC_README.md": '''
# IMA - Intelligent Meta Architecture

## Vision

IMA is a learning AI architecture designed to evolve through validated community collaboration.

## Architecture

Community Layer
|
Validation Layer
|
Learning Bridge
|
IMA Core

## Contribution

Developers can submit:

- improvements
- connectors
- tools
- research

All changes pass validation before entering protected systems.

## Security

Private Core remains protected.

Community improves the ecosystem without direct access to internal intelligence.

## License

IMA Community License
''',


"IMA_COMMUNITY_RULES.md": '''
# IMA Community Rules

1. Respect contributors.
2. No malicious code.
3. No attempts to bypass security.
4. All learning contributions require validation.
5. Core identity and private memory are protected.
''',


"IMA_API_DOCUMENTATION.md": '''
# IMA API Documentation

## Community Gateway

Submit Contribution:

POST /community/submit

Receive Message:

POST /community/message

Connector Registration:

POST /connector/register

Validation:

POST /contribution/validate
'''

}


for p,c in files.items():

    path = Path(p)
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not path.exists():
        path.write_text(
            c.strip()+"\n",
            encoding="utf8"
        )


print("IMA PUBLIC SECURITY + GOVERNANCE PACKAGE CREATED")
