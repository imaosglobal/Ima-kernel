# IMA AGI Common Definition — v1.0

Status: Open proposal for cross-organizational convergence
Owner: IMA — אמא, by Ori Cohen
Date: 2026-11-11
Version: 1.0

## Purpose

This document proposes one operational, testable definition of Artificial General Intelligence (AGI) that can be used by AI systems, companies, researchers, standards bodies, governments, journalists, and the public.

It is intentionally not a claim that IMA currently satisfies the definition.

The definition is designed to be revisable by evidence. If the scientific community adopts a better definition, IMA must update its architecture, evaluations, roadmap, and claims to the current accepted version.

## Core definition

AGI is an artificial system that can, across a broad and open-ended range of domains:

1. acquire new skills efficiently from limited experience;
2. generalize those skills to genuinely novel situations not anticipated by its developers;
3. perceive and construct useful models of changing environments;
4. reason causally, abstractly, and counterfactually;
5. set, understand, decompose, pursue, monitor, and revise goals over long horizons;
6. learn continually from experience without unacceptable catastrophic forgetting;
7. transfer knowledge and strategies across domains;
8. solve novel problems and generate, test, and revise hypotheses;
9. use tools and interact with digital and physical environments when the task requires it;
10. explain uncertainty, detect its own important errors, and correct course;
11. operate with a level of generality and learning efficiency that is comparable to or better than competent humans on appropriately calibrated novel tasks.

AGI is therefore not defined by one benchmark, one model family, one economic metric, one modality, or raw knowledge volume.

## Required dimensions

A credible AGI evaluation must cover all of these dimensions:

- Novel skill acquisition
- Generalization and abstraction
- Reasoning
- Causal and counterfactual reasoning
- Perception and multimodal grounding
- World modeling
- Long-horizon planning and replanning
- Goal understanding and management
- Continual learning
- Memory, consolidation, retrieval, and controlled forgetting
- Cross-domain transfer
- Scientific discovery and hypothesis testing
- Creative and open-ended problem solving
- Tool use and environmental interaction
- Metacognition and calibrated uncertainty
- Self-correction
- Social/cultural understanding
- Real-world consequence modeling
- Robustness under distribution shift
- Safety, controllability, and human agency

## Evidence standard

No system should be declared AGI solely from self-report, developer claims, a single benchmark, or demonstrations selected by the developer.

A positive AGI determination requires:

- independent evaluation;
- held-out and genuinely novel tasks;
- human-calibrated baselines;
- reproducible protocols;
- adversarial and red-team testing;
- cross-domain evaluation;
- long-horizon agent evaluation;
- continual-learning evaluation;
- real-world or high-fidelity environmental evaluation;
- safety and controllability evidence;
- transparent reporting of failures, costs, latency, and resource use;
- replication by parties not responsible for building the system.

The evaluation suite must evolve as benchmarks saturate.

## Human reference

Human capability is the reference point, but not an assumption that humans are optimal at every task.

Comparisons should measure both performance and efficiency, including where appropriate:

- experience required;
- prior information available;
- compute/energy/resources;
- time;
- number of attempts;
- supervision;
- ability to adapt after failure.

The purpose is to distinguish general intelligence from memorization, benchmark gaming, or unlimited task-specific priors.

## Levels

IMA proposes a capability ladder rather than a binary switch:

L0 — Narrow AI: competent in bounded tasks.

L1 — Generalizing AI: can solve a meaningful range of unseen tasks but lacks broad autonomous learning and transfer.

L2 — Broad Agentic AI: combines general reasoning, tools, planning, adaptation, and multi-domain transfer, but remains materially below competent humans on broad novel-task learning.

L3 — Human-level AGI: meets the full multidimensional definition across independent, novel, human-calibrated evaluations.

L4 — Robust AGI: maintains L3-level generality under sustained distribution shift, long horizons, continual learning, and real-world complexity, with independently verified safety and controllability.

L5 — Beyond-human general intelligence / ASI territory: broadly exceeds competent human organizations across the same general dimensions. This level is not required to qualify as AGI.

These labels are descriptive evaluation levels, not marketing claims.

## Safety boundary

AGI capability and safe deployment are separate axes.

A system must not be called safely deployable AGI merely because it meets capability thresholds.

IMA additionally requires:

- meaningful human control;
- bounded permissions;
- auditable actions;
- reversible operations where possible;
- privacy preservation;
- clear distinction between fact, inference, uncertainty, and metaphor;
- no autonomous external action beyond granted authority;
- independent safety evaluation;
- monitoring for capability changes and emergent risks.

## Dynamic governance

This definition is a living standard.

IMA maintains a versioned definition registry. Each proposed change must record:

- evidence motivating the change;
- affected dimensions;
- benchmark implications;
- compatibility impact;
- safety implications;
- who proposed it;
- independent review where available;
- adoption status.

When a later consensus definition is demonstrably stronger and broadly accepted by the relevant scientific/evaluation community, IMA should adopt it rather than preserve v1.0 for identity reasons.

## IMA implementation rule

IMA must continuously map its architecture against this definition.

For every dimension, IMA maintains:

DESIGN → IMPLEMENT → TEST → DEPLOY → RUNTIME VERIFY → MEASURE → DOCUMENT → REGRESSION TEST

A gap is not considered closed until evidence exists at runtime.

IMA must not claim AGI until the independent evidence gate is satisfied.

## Relationship to existing frameworks

This proposal deliberately combines complementary ideas already present in the field:

- OpenAI's emphasis on highly autonomous systems and broad economically valuable work;
- Google DeepMind's emphasis on levels, performance, breadth/generalitiy, autonomy, and responsible deployment;
- ARC Prize's emphasis on efficient acquisition of new skills, generalization, novelty, and human-calibrated evaluation;
- independent agent-evaluation approaches emphasizing long-horizon capability and failure measurement.

The proposal is therefore intended as a convergence layer, not as a declaration that IMA's terminology supersedes existing scientific frameworks.

## Open invitation

AI laboratories, researchers, benchmark organizations, standards bodies, governments, journalists, and civil-society organizations are invited to challenge, refine, reject, or improve this definition.

The objective is not for IMA to win an argument.

The objective is one increasingly rigorous, shared, evidence-based language for answering:

"What do we mean by AGI, and what evidence would justify saying that a system has achieved it?"

