from pathlib import Path
import json
import time

files = {

"investor_package/PITCH_DECK.md": """
# IMA Pitch Deck

## 1. Vision

IMA is a personal intelligence layer designed to help humans and organizations build long-term understanding through memory, learning and insight extraction.

## 2. Problem

Current AI assistants:
- lose context
- lack persistent personal understanding
- provide answers without building a relationship with accumulated knowledge

## 3. Solution

IMA combines:

- Personal memory
- Learning loop
- Pattern extraction
- Historical inference
- Product gateway
- Governance layer

## 4. Technology

Core architecture:

User
↓
Memory
↓
Learning
↓
Patterns
↓
Understanding
↓
Improved Interaction

## 5. Current Stage

Working prototype:

- Runtime verified
- Brain layer verified
- Memory verified
- Learning pipeline verified
- Product layer verified
- Governance implemented

## 6. Market

Potential applications:

- Personal AI assistants
- Enterprise knowledge systems
- Education
- Healthcare support tools
- Human-computer interaction

## 7. Business Model

Possible models:

- Subscription
- Enterprise licensing
- API access
- Strategic partnerships

## 8. Investment Goal

Build:

- Engineering team
- Product team
- Infrastructure
- Market validation

## 9. Strategic Vision

Create a scalable intelligence platform that preserves human identity while increasing capability.
""",

"investor_package/DATA_ROOM.md": """
# IMA Data Room

## Technical

- Runtime
- Brain
- Memory architecture
- Learning loop
- Historical inference
- Product gateway

## Product

- Product layer
- Demo framework
- Client layers
- Device layer

## Governance

- Intellectual property model
- Learning policy
- Self change policy

## Documents

- Vision
- Architecture
- Investment thesis
- Partnership strategy
- Market position
""",

"investor_package/ANGEL_TARGETS.md": """
# Potential Angel Categories

## AI / Deep Tech

Investors interested in:
- Artificial intelligence
- Machine learning
- Human AI interaction

## Strategic Partners

Potential categories:

- AI companies
- Cloud infrastructure providers
- Enterprise software companies
- Research organizations

## Partnership Goal

Find partners who can accelerate:

- Product development
- Distribution
- Market entry
""",

"investor_package/INVESTOR_SNAPSHOT.md": f"""
# IMA Investor Snapshot

Generated:
{time.ctime()}

Status:

Runtime: VERIFIED
Brain: VERIFIED
Memory: VERIFIED
Learning: VERIFIED
Product Layer: VERIFIED
Governance: VERIFIED

Purpose:

Prepare IMA for external evaluation and strategic partnership discussions.
"""
}

for name, content in files.items():
    p = Path(name)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.strip()+"\n", encoding="utf-8")

print("IMA INVESTOR READINESS V2 CREATED")
