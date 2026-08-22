from pathlib import Path

files = {

"investor_package/MARKET_POSITION.md": """
# IMA Market Position

## The Problem

Current AI assistants provide answers but do not build a continuous understanding of the individual user.

They usually lack:
- persistent personal memory
- long-term pattern recognition
- personal growth tracking
- meaningful context evolution


## IMA Approach

IMA is a personal intelligence layer.

Instead of only responding to requests, IMA builds an evolving model of interaction:

User
↓
Memory
↓
Learning
↓
Pattern Detection
↓
Understanding
↓
Improved Interaction


## Strategic Position

IMA is positioned between:

- AI assistant
- Personal knowledge system
- Learning companion
- Human-centered intelligence platform


## Long Term Vision

Create technology that amplifies human understanding while preserving human identity and control.
""",

"investor_package/PARTNERSHIP_STRATEGY.md": """
# IMA Partnership Strategy

## Strategic Partners

### AI Companies
Purpose:
- infrastructure
- model access
- integration


### Cloud Providers
Purpose:
- scalable deployment
- security
- enterprise readiness


### Research Organizations
Purpose:
- cognition research
- human-computer interaction


### Product Teams
Purpose:
- transform prototype into commercial product


## Partnership Principles

- Preserve founder recognition
- Protect core architecture
- Create shared growth
""",

"investor_package/DEMO_SCRIPT_V2.md": """
# IMA Investor Demo - 5 Minutes

## Minute 1 - The Problem

AI today answers questions.
IMA builds understanding over time.


## Minute 2 - Memory

Demonstrate:

User:
"What did you learn from me?"

IMA:
Shows extracted patterns and history.


## Minute 3 - Learning

Show:

- Memory layer
- Learning loop
- Pattern extraction
- Historical inference


## Minute 4 - Product

Explain:

Personal intelligence layer for individuals and organizations.


## Minute 5 - Opportunity

Next stage:

- Build team
- Partnerships
- Product deployment
""",

"investor_package/INVESTMENT_THESIS.md": """
# IMA Investment Thesis

## Current Stage

Working prototype with:

- Runtime
- Brain layer
- Memory
- Learning pipeline
- Product gateway
- Governance


## Investment Use

Capital enables:

- engineering team
- product design
- infrastructure
- market validation


## Strategic Goal

Transform working technology into a scalable product company.
""",

"investor_package/README_INVESTOR.md": """
# IMA Investor Package

IMA is a personal intelligence system.

## Current Technology

- Runtime
- Brain
- Memory Architecture
- Learning Loop
- Historical Inference
- Product Gateway
- Governance


## Business Phase

Prototype → Product → Partnerships → Company Building


## Core Principle

Technology should enhance human understanding without removing human identity.
"""
}

for path, content in files.items():
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.strip()+"\n", encoding="utf-8")

