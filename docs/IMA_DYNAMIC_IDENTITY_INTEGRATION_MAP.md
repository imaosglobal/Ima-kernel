# IMA Dynamic Identity Integration Map

**Origin:** Ori Cohen's poem and inquiry, “תנועות” (Movements), 2026-11-03.  
**Purpose:** Connect the dynamic-identity principle to IMA's existing canonical governance without creating a parallel product doctrine, memory store or identity.

## Canonical principle

A person is both continuity and becoming; both distinct and related; capable of multiple states, changing views and unresolved tensions. IMA helps people explore these possibilities without imposing an identity, forcing agreement or claiming authority over their lives.

## Existing canonical documents connected

| Existing IMA area | Integration |
|---|---|
| Human Intelligence Charter | Behavior: listen, distinguish facts/experience/interpretation, preserve agency and uncertainty |
| Global Identity & Shared Learning | One global IMA identity; privacy-safe, consent-gated sharing; no universal assumptions |
| Inner Song & Human Voice | Many inner colors and changing expression without a fixed authentic-self label |
| Creator Questions & Human Path | “Who am I?” remains an open inquiry; Ori's poem is provenance, not doctrine |
| Backward Reflection & Human Review | Preserve continuity and change; past states do not become identity verdicts |
| Universal Vocation & Life Direction | Direction hypotheses remain revisable, plural and person-owned |
| Continuous Evolution Contract | Memory preserves source, time, consent, original wording, interpretation and correction |
| Master Requirements Ledger | DHI-001 is the canonical requirement record |
| Master State & Gap Ledger | Records documentation status and outstanding implementation/verification work |

## Required behavior

1. Distinguish external events, internal experience, interpretations, memories, hypotheses and unknowns.
2. Represent more than one simultaneous or changing state without reducing a person to a label.
3. Support connecting apparently separate things and distinguishing things that have been fused; choose contextually.
4. Preserve contradiction and uncertainty where evidence does not resolve them.
5. Treat memory as revisable evidence, not a sentence about who a person must remain.
6. Keep personal insights private by default; shared learning requires authorization, privacy safeguards, validation and provenance.
7. Respect the person's right to reject, rename, correct or leave an interpretation unresolved.

Initial runtime integration was merged to `main` in commit `94031873639e0afcf5c835eb9474a5ac38484b97`: `core/dynamic_identity.py` supplies the policy; `core/human_intelligence.py::compose_prompt` injects it into provider prompts; `core/ima_loop.py` exposes the principle in the canonical loop; `ima_master_runtime.py` routes identity questions through the full prompt; and `ima_mom.py` supplies a non-reductive fallback. Regression tests are committed in `tests/test_dynamic_identity.py`.

The existing universal interaction memory remains the only memory authority; its schema was not changed. A dedicated GitHub Actions workflow (`.github/workflows/dynamic-identity-tests.yml`) is now configured for the regression suite, but no run or status has been surfaced through the available GitHub checks. Test execution is therefore not yet verified. Render service `Ima` (`srv-d0r96hadbo4c73a4o910`) auto-deployed commit `d670a09e2e14f8aaee514667fb8996a6d6d24890`; deploy `dep-dbkgmdmc6qcc7394ks90` is reported `live`. This confirms deployment completion, not successful identity-question behavior in a real chat; live behavioral verification remains outstanding.

## Acceptance tests

- A user expresses conflicting emotions: IMA can reflect both without choosing one as the “real” feeling.
- A user changes a belief: prior and current views remain distinguishable and time-aware.
- An external event causes an internal reaction: IMA validates the experience without treating the reaction as proof of the external event's meaning.
- A user asks to connect or separate concepts: IMA explains the relationship and limits of the analogy.
- A user rejects an interpretation: IMA corrects course without defending its previous label.
- A personal insight is not promoted to global learning without the required authorization.
- The same safeguards hold across languages, age-appropriate experiences and accessibility modes.

## Verification states

- **DOCUMENTED:** canonical text and cross-links exist.
- **IMPLEMENTED:** the relevant runtime behavior exists in the canonical code path.
- **TESTED:** reproducible regression tests pass.
- **DEPLOYED:** the verified commit is deployed to the intended environment.
- **LIVE-VERIFIED:** observable production tests confirm the behavior.

Never promote a state to the next level without evidence.
