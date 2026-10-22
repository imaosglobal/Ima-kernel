# IMA System Truth & Capability Map

Status: canonical governance/verification specification. This document does not claim capabilities are live merely because they are specified.
Date: 2026-10-22

## Purpose
Provide one cross-domain evidence model for IMA. Every capability has a lifecycle state and must be supported by evidence before being described as verified.

## Status values
- PLANNED — specified but not implemented or tested.
- ATTEMPTED — an implementation or test was attempted; outcome is not yet sufficient for verification.
- EXECUTED — an authorized change or action was actually performed.
- VERIFIED — execution or capability is supported by reproducible evidence.
- FAILED — an attempted change/test failed.
- GAPS_RECORDED — the missing evidence, dependency or authorization is explicitly recorded.

## Evidence rule
Code presence, configuration, eligibility, a URL, a button, a follower/view count, an account, or a deployment dashboard does not by itself prove operational success. Verification requires the smallest sufficient reproducible evidence for the capability.

## Canonical capability domains
1. Identity & access
2. Memory & provenance
3. Reasoning & evidence
4. Learning & teaching
5. Web/research
6. Vision
7. Voice/audio
8. Avatar/video
9. Communication/distribution
10. Creator & commerce
11. Finance & expenses
12. Nonprofit governance
13. Creator rights & succession
14. Safety, privacy & consent
15. Human-agency controls
16. Accessibility & multilingual UX
17. Community/public benefit
18. Continuity & portability

## Promotion rule
A capability may be promoted to VERIFIED only when its required evidence exists. If evidence disappears, expires, or becomes contradicted, the status must be downgraded rather than guessed.

## Canonical truth language
Use: verified, partially verified, attempted, blocked, not yet verified, or unknown. Do not use "live", "working", "connected", "earning", "registered nonprofit", or equivalent claims unless evidence supports that exact claim.

## Human agency
The map is descriptive and auditable. It never grants IMA authority to spend, contract, transfer, publish consequential material, alter canonical memory, or change legal/creator rights autonomously.
