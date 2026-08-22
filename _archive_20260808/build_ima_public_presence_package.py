from pathlib import Path

files = {

"README.md": '''
# IMA - Intelligent Meta Architecture

## Vision

IMA is a modular AI architecture designed for collaborative evolution.

Community contributions improve the ecosystem through controlled validation.

## Architecture

Public Community Layer

        |
        v

Validation Gateway

        |
        v

Learning Bridge

        |
        v

Protected Core


## Contributing

Developers can contribute:

- connectors
- tools
- research
- improvements
- integrations


## Security Model

Public contributors cannot access:

- private memory
- identity systems
- internal reasoning
- security credentials


## Philosophy

Open collaboration.
Protected intelligence.
Continuous improvement.
''',


"docs/ARCHITECTURE.md": '''
# IMA Architecture

Layers:

1. Community Layer
2. Connector Layer
3. Validation Layer
4. Learning Bridge
5. Private Core


Every external contribution passes validation.
''',


"docs/DEVELOPER_GUIDE.md": '''
# IMA Developer Guide


## Create Connector

A connector should:

- receive external events
- normalize information
- respect security policies


## Contribution Flow


Developer

↓

Submission

↓

Sandbox

↓

Validation

↓

Learning Bridge

↓

Release
''',


"docs/API.md": '''
# IMA API


## Community Message

POST /community/message


## Submit Contribution

POST /community/submit


## Register Connector

POST /connector/register


## Validate Change

POST /contribution/validate
''',


"community/RULES.md": '''
# IMA Community Rules


1. Respect contributors.

2. No malicious code.

3. No attempts to bypass security.

4. All changes require validation.

5. Private Core remains protected.
''',


"developer_portal/index.md": '''
# IMA Developer Portal


Sections:


- Documentation

- API Reference

- Connector SDK

- Contribution System

- Security Rules

- Community
''',


"LICENSE_IMA_COMMUNITY.md": '''
# IMA Community License


Community Edition:

Open for collaboration.


Private Core:

Protected.


Changes:

Accepted through validation process.
'''
}


for path,content in files.items():

    p=Path(path)

    p.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    p.write_text(
        content.strip()+"\n",
        encoding="utf8"
    )


