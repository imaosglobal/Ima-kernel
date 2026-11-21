# IMA Capability Migration Status — 2026-11-21

## Canonical rule

All useful legacy capabilities are adapted into `imaosglobal/Ima-kernel`. Source repositories remain provenance/evidence sources and are not treated as parallel brains, memory authorities, feedback authorities, or LIVE-001 runtimes.

## Completed in this migration wave

### ima-os-evolving-home
- Permanent quality concepts → `learning/permanent_quality_guard.py`
- Self-improvement observation concepts → `learning/self_improvement_signals.py`
- Tests added for both.
- Aggressive autonomous background mutation was intentionally not migrated.

### Ima-server
- Public MCP status/learning/distribution contract → `runtime/mcp_public_status_adapter.py`
- Tests added.
- The adapter is read-only and does not expose private memory/secrets.
- The host entitlement blocker remains external to the repository.

### Ima-self-deploy
- Deterministic deployment health checks → `deployment/health_contract.py`
- Tests added.
- Legacy secret loading, Docker mutation, package installation and process killing were intentionally excluded.

### Ima-3d-mom
- Semantic intent adapter was previously migrated with explicit confirmation boundaries.
- Legacy file-based memory and duplicate action dispatcher were intentionally excluded.

## Not promoted to live capability

Every new migration is recorded as `IMPLEMENTED_IN_CODE / TESTED_PENDING_CI` until reproducible CI or equivalent verification is available. No capability is promoted to VERIFIED_LIVE merely because source code exists.

## Remaining provenance-only areas

- `ima-core-experience`: its product specification is largely architectural/product-direction material; no unique runtime contract was promoted without sufficient implementation evidence.
- `Imamvp`, `Ima-all-in-one`, `Ima`: historical/prototype concepts remain mapped as provenance unless a concrete unique capability can be demonstrated.
- Empty repositories remain empty.
- `react` and `pytorch` remain unrelated upstream/vendor mirrors unless future evidence proves IMA-specific modifications.

## Safety boundary

No credentials, `.env` values, private data, stale backup implementations, autonomous mutation loops, or duplicate runtime authorities were copied into the canonical kernel.
