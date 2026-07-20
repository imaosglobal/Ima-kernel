# IMA Automated Maintenance

## Purpose

Automated validation gate for the active IMA system.

## Pipeline

1. BOOT
   - Runs the canonical single-entry boot validation.
   - Verifies canonical policy, hashes, fallback state, and canonical registry.

2. ACTIVE_COMPILE
   - Compiles the active Python code areas:
     - kernel/
     - .ima/CANONICAL_AUTHORITY/
     - .ima/agi_evolution/

3. SYSTEM READY
   - Printed only when all checks pass.

## Safety Boundary

This component is a validation/orchestration layer.

It does not:
- modify canonical hashes;
- modify the canonical registry;
- modify source code automatically;
- touch archive or backup files.

Future repair automation should use:
validate -> snapshot -> repair -> validate -> rollback on failure.

## Status

Validated successfully before relocation.
