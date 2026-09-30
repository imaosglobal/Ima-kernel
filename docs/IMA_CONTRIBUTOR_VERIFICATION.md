# IMA Contributor Verification

From a clean checkout, run:

```bash
npm run ima:verify
```

The command runs the core test, canonical integrity/runtime checks, public runtime isolation tests, the contract harness, and the reproducible accessibility contract.

Expected final marker:

```
IMA_VERIFY=PASS
```

The command is read/test-only: it must not publish secrets, modify source files, or delete project data.
