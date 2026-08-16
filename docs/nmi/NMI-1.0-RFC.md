# NMI-1.0 — Minimum Necessary Invasiveness
## Open Standard Proposal / RFC

### 0. Status of this document
This document is a public technical proposal. It is not an approved medical standard and must not be represented as one.

Normative terms:
- **MUST** — mandatory for conformance to this proposal.
- **SHOULD** — recommended unless a documented reason exists.
- **MAY** — optional.

### 1. Problem statement
Healthcare uses multiple routes for delivering medicines and biological products. Some require needles or other invasive access. Existing standards address particular device classes, but there is an opportunity for a cross-technology framework that makes invasiveness a first-class design and comparison attribute.

### 2. Objective
NMI establishes a common vocabulary and evaluation framework for selecting and developing the least-invasive clinically suitable delivery route.

### 3. Fundamental principle
A delivery route MUST NOT be considered preferable solely because it is less invasive. It must be evaluated jointly for:
- clinical effectiveness
- safety
- dose accuracy
- delivery reliability
- pharmacokinetic suitability where relevant
- usability
- human factors
- manufacturability
- infection/cross-contamination risk
- environmental impact
- lifecycle cost

When clinically equivalent alternatives exist, the proposal recommends preference for the lower-invasiveness option.

### 4. Invasiveness classification
N0 — External/non-contact or fully external treatment interface.
N1 — External contact without tissue penetration.
N2 — Minimal/limited tissue penetration.
N3 — Significant tissue penetration.
N4 — Invasive access to internal tissue, vessel, cavity, or organ.

The classification is descriptive, not a claim of clinical safety.

### 5. Delivery-selection model
A conforming system SHOULD represent:

Drug/Therapy Profile
→ Candidate Delivery Routes
→ Safety/Efficacy Constraints
→ Delivery Performance Requirements
→ Route Selection
→ Controlled Delivery
→ Monitoring
→ Fail-safe response
→ Traceable record

No autonomous system should select or alter a patient's treatment solely from an NMI score.

### 6. Minimum performance dimensions
A candidate route SHOULD be assessed against:
1. delivered dose accuracy
2. delivery-rate stability
3. delivery-site consistency
4. repeatability
5. adverse-event profile
6. user burden
7. pain/discomfort where relevant
8. device reliability
9. contamination control
10. failure detection
11. emergency/stop behavior
12. storage and stability requirements
13. waste
14. accessibility and usability

### 7. Fail-safe principle
A delivery system MUST have a defined safe state for detected malfunction or clinically relevant uncertainty, appropriate to its intended use.

### 8. Evidence hierarchy
Claims should be supported progressively by:
- engineering verification
- laboratory testing
- appropriate preclinical evidence
- human factors studies
- clinical investigation
- post-market evidence

The level required depends on the intended use and regulatory classification.

### 9. Interoperability
NMI SHOULD allow a delivery technology to be evaluated without requiring the same physical mechanism across products.

### 10. Future technology neutrality
NMI MUST remain technology-neutral. It must not prescribe a particular physical mechanism such as pressure, ultrasound, electrical stimulation, microneedles, or another modality.

### 11. Regulatory compatibility
NMI does not replace applicable medical-device, drug, combination-product, quality-management, risk-management, or clinical requirements.

### 12. Conformance statement
A product or research system may state:
“Evaluated against NMI-1.0 Public Draft”
only if the evaluation record identifies:
- version
- scope
- intended use
- applicable requirements
- evidence
- deviations
- reviewer/organization

It MUST NOT state “NMI certified” unless a future independent conformity-assessment scheme formally exists.

### 13. Open questions for expert review
- Is the N0–N4 taxonomy sufficiently useful?
- Which performance metrics should be mandatory?
- How should invasiveness be weighted against efficacy and safety?
- Should NMI be a standalone standard or a framework referencing existing device-specific standards?
- What should be the boundary between drug-delivery standards and clinical-practice guidelines?
- Which international committee is the optimal home for future work?

### 14. Proposed revision process
Every major revision should include:
- public issue tracking
- evidence review
- conflict-of-interest declaration
- documented disposition of substantive comments
- versioned publication
- change log

### 15. Authorship, attribution and rights

This proposal identifies **Ori Cohen** as its human originator and author. The proposal was developed with assistance from **OpenAI's ChatGPT (GPT-5.6 Luna)**, which is disclosed for transparency and is not represented as a human co-author or rights holder.

The publication of this proposal does not intentionally assign, transfer, waive, or surrender any rights Ori Cohen may have in his original contributions or other protectable material. Nothing in this document grants ownership of third-party material incorporated by reference.

For patentable technical inventions, trademark rights, confidential know-how, or other rights requiring formal legal action, publication alone may affect legal options. Appropriate professional intellectual-property advice should be obtained before public disclosure of any potentially patentable implementation.
