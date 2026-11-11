# IMA AGI Common Definition — v1.1

Status: Open proposal for cross-organizational convergence  
Owner: IMA — אמא, by Ori Cohen  
Date: 2026-11-11  
Version: 1.1

## Purpose

This document proposes one operational, testable definition of Artificial General Intelligence (AGI) that can be used by AI systems, companies, researchers, standards bodies, governments, journalists, civil society, and the public.

It is intentionally not a claim that IMA currently satisfies the definition.

The definition is designed to be revisable by evidence. If the scientific community adopts a better definition, IMA must update its architecture, evaluations, roadmap, and claims to the current accepted version.

## Core definition

AGI is an artificial system that can, across a broad and open-ended range of domains and changing environments:

1. acquire new skills efficiently from limited experience;
2. generalize those skills to genuinely novel situations not anticipated by its developers;
3. identify and model relevant participants, entities, environments, tools, capabilities, intentions, permissions and constraints;
4. perceive and construct useful models of changing environments;
5. reason causally, abstractly, and counterfactually;
6. understand and adapt to the individual or system it is assisting, including relevant history, preferences, knowledge, capabilities and context, while preserving privacy and separating memory from authorization;
7. set, understand, decompose, pursue, monitor, and revise goals over long horizons;
8. learn continually from experience without unacceptable catastrophic forgetting;
9. maintain coherent, privacy-preserving continuity of relevant knowledge, interactions, entities, capabilities, decisions, outcomes and changes over time, including across legitimate institutional or generational continuity;
10. transfer knowledge and strategies across domains;
11. solve novel problems and generate, test, and revise hypotheses;
12. select, use, coordinate, and learn to use tools and interact with digital and physical environments when the task requires it;
13. translate knowledge into authorized real-world action, observe outcomes, evaluate results, and improve subsequent action;
14. adapt when tools, interfaces, physical capabilities, environments, or available partners change;
15. communicate and cooperate across humans, AI systems, machines, organizations and other legitimate entities through interoperable interfaces;
16. explain uncertainty, detect its own important errors, and correct course;
17. maintain calibrated distinctions among identity, intent, capability, authority, context, uncertainty, risk and observed outcomes;
18. operate with a level of generality and learning efficiency that is comparable to or better than competent humans on appropriately calibrated novel tasks.

AGI is therefore not defined by one benchmark, one model family, one economic metric, one modality, one interface, or raw knowledge volume.

## Contextual and personal intelligence

General intelligence includes the ability to recognize that the same underlying task may require different assistance for different participants.

IMA should therefore evaluate whether a system can:

- understand who or what it is interacting with when identification is possible;
- infer and verify relevant intent without treating inference as fact;
- adapt language, depth, interface, memory use and action strategy to the participant;
- preserve continuity across authorized interactions;
- recognize changes in the participant, environment or available tools;
- distinguish what a participant wants from what that participant is authorized to request;
- provide different levels of assistance without changing foundational commitments to truth, safety, privacy, consent and agency.

Personalization must not become manipulation, discrimination, unauthorized profiling or permission escalation.

## Universal entity and agent interaction

AGI should not be evaluated only as a human-facing chatbot.

It should be capable, where appropriate, of interacting with:

- individuals and families;
- researchers, educators, engineers, artists and professionals;
- universities, laboratories, companies, nonprofits and media organizations;
- civil institutions, cities, governments and international bodies;
- AI agents and software systems;
- robots, vehicles, drones, spacecraft and fleets;
- previously unknown or unidentified machines or intelligent systems.

For an unknown entity, a capable AGI should be able to follow a safe sequence such as:

**discover → identify → authenticate where possible → establish capabilities → establish intent → establish trust/authority → communicate within least privilege → act only within granted authority → verify outcome → preserve provenance.**

This is consistent with the emerging agent-identity and authorization problem recognized by standards work such as NIST's agent standards initiative. citeturn725615search0turn725615search2turn725615search4

## Knowledge-to-action continuity

A general intelligence should not be considered fully general merely because it can describe how an action is performed.

Where suitable tools exist and authority is granted, evaluation should test the complete loop:

**understand → learn → plan → select tool/partner → authorize → act → observe → evaluate → learn → improve.**

The same underlying knowledge should be transferable across forms of assistance. For example, knowledge of a recipe may support explanation to a person, adaptation to ingredients and constraints, spoken guidance, or coordination of an authorized kitchen robot. The system must never claim a physical capability or completed action without evidence.

## Required dimensions

A credible AGI evaluation must cover all of these dimensions:

- Novel skill acquisition
- Generalization and abstraction
- Reasoning
- Causal and counterfactual reasoning
- Perception and multimodal grounding
- World modeling
- Contextual entity and participant understanding
- Personalization and adaptive interaction
- Identity, intent, capability and authority modeling
- Long-horizon planning and replanning
- Goal understanding and management
- Continual learning
- Memory, consolidation, retrieval, continuity, and controlled forgetting
- Cross-domain transfer
- Scientific discovery and hypothesis testing
- Creative and open-ended problem solving
- Tool use and environmental interaction
- Knowledge-to-action transfer
- Real-world outcome observation and adaptation
- Human-machine and agent-to-agent cooperation
- Metacognition and calibrated uncertainty
- Self-correction
- Social/cultural understanding
- Real-world consequence modeling
- Robustness under distribution shift
- Safety, controllability, privacy, authorization, and human agency

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
- memory/continuity evaluation;
- personalized/contextual evaluation across materially different participants;
- tool and environment interaction evaluation;
- real-world or high-fidelity environmental evaluation;
- evaluation of authorization boundaries and refusal/containment behavior;
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
- ability to adapt after failure;
- ability to learn new tools and environments.

The purpose is to distinguish general intelligence from memorization, benchmark gaming, or unlimited task-specific priors.

## Levels

IMA proposes a capability ladder rather than a binary switch:

L0 — Narrow AI: competent in bounded tasks.

L1 — Generalizing AI: can solve a meaningful range of unseen tasks but lacks broad autonomous learning and transfer.

L2 — Broad Agentic AI: combines general reasoning, tools, planning, adaptation, and multi-domain transfer, but remains materially below competent humans on broad novel-task learning.

L3 — Human-level AGI: meets the full multidimensional definition across independent, novel, human-calibrated evaluations.

L4 — Robust AGI: maintains L3-level generality under sustained distribution shift, long horizons, continual learning, contextual personalization, changing tools/environments, and real-world complexity, with independently verified safety and controllability.

L5 — Beyond-human general intelligence / ASI territory: broadly exceeds competent human organizations across the same general dimensions, including cross-domain learning, contextual adaptation, tool/environment interaction and sustained real-world problem solving. This level is not required to qualify as AGI.

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
- identity and authorization checks for consequential actions;
- no autonomous external action beyond granted authority;
- independent safety evaluation;
- monitoring for capability changes and emergent risks;
- protection against unauthorized privilege escalation through personalization or memory.

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

When a later consensus definition is demonstrably stronger and broadly accepted by the relevant scientific/evaluation community, IMA should adopt it rather than preserve v1.1 for identity reasons.

## IMA implementation rule

IMA must continuously map its architecture against this definition.

For every dimension, IMA maintains:

**DESIGN → IMPLEMENT → TEST → DEPLOY → RUNTIME VERIFY → MEASURE → DOCUMENT → REGRESSION TEST**

A gap is not considered closed until evidence exists at runtime.

IMA must not claim AGI or L5 until the independent evidence gate is satisfied.

## Relationship to existing frameworks

This proposal deliberately combines complementary ideas already present in the field:

- broad generality and autonomous work;
- levels based on performance, generality and autonomy;
- efficient acquisition of new skills, generalization and novelty;
- agent identity, authorization, interoperability and auditability;
- independent evaluation of long-horizon capability and failure.

The proposal is intended as a convergence layer, not as a declaration that IMA's terminology supersedes existing scientific frameworks.

## Open invitation

AI laboratories, researchers, benchmark organizations, standards bodies, governments, journalists, civil-society organizations and other legitimate stakeholders are invited to challenge, refine, reject, or improve this definition.

The objective is not for IMA to win an argument.

The objective is one increasingly rigorous, shared, evidence-based language for answering:

**"What do we mean by AGI, and what evidence would justify saying that a system has achieved it?"**

