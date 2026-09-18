# IMA Autonomous Operating Contract

Purpose: maintain IMA as a continuously verified system rather than a sequence of manual fixes.

## Loop
1. Observe: GitHub Actions, deployment health, build artifacts and declared external integrations.
2. Diagnose: use actual logs and exact failing component; distinguish root cause from symptom.
3. Change: smallest reversible change; never overwrite unrelated local work.
4. Verify: run the affected build/test/health checks.
5. Record: commit the verified change and preserve provenance.
6. Repeat: scheduled health checks continue independently.

## Source of truth
GitHub repository and verified deployment state are authoritative for engineering state. Gmail is an optional notification/evidence channel, not the engineering source of truth.

## Integration rule
New AI models, APIs and tools enter through capability discovery, adapter/connector, validation, provenance and registry update. No provider becomes a silent dependency.

## Failure rule
No failure is declared fixed until the failing check passes after the change. No email notification alone is treated as proof of failure or recovery.

## Safety
No secrets in source control. No destructive automatic cleanup of user work. No autonomous modification of credentials, billing, production data, or external accounts.
