from pathlib import Path
import py_compile
import shutil
from datetime import datetime

P = Path(".ima/research/ima_research_council.py")

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = (
    P.parent / "backups" /
    f"ima_research_council_before_meda_hardening_v55_{stamp}.py"
)
backup.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(P, backup)

text = P.read_text(encoding="utf-8")

old = '''        executor = ThreadPoolExecutor(
            max_workers=1
        )

        future = executor.submit(
            self._run_agent,
            agent_name,
            question,
            subquestion_id,
            previous_results
        )

        try:

            return future.result(
                timeout=timeout
            )

        except TimeoutError:
'''

new = '''        executor = ThreadPoolExecutor(
            max_workers=1
        )

        future = executor.submit(
            self._run_agent,
            agent_name,
            question,
            subquestion_id,
            previous_results
        )

        try:

            return future.result(
                timeout=timeout
            )

        except TimeoutError:
'''

if old not in text:
    raise SystemExit("ERROR: timeout dispatcher anchor not found")

# The real architectural fix is in the outer executor:
# replace the context manager with an explicit executor so that
# completed results are consumed without an implicit shutdown(wait=True).

old_outer = '''        with ThreadPoolExecutor(
            max_workers=max(
                1,
                len(jobs)
            )
        ) as pool:
            futures = {}

            for agent_name, q, sid in jobs:
                future = pool.submit(
                    self._run_with_timeout,
                    agent_name,
                    q,
                    sid,
                    previous_results
                )

                futures[future] = (
                    agent_name,
                    sid
                )

            for future in as_completed(
                futures
            ):
'''

new_outer = '''        pool = ThreadPoolExecutor(
            max_workers=max(
                1,
                len(jobs)
            )
        )

        futures = {}

        for agent_name, q, sid in jobs:
            future = pool.submit(
                self._run_with_timeout,
                agent_name,
                q,
                sid,
                previous_results
            )

            futures[future] = (
                agent_name,
                sid
            )

        try:
            for future in as_completed(
                futures
            ):
'''

if old_outer not in text:
    raise SystemExit("ERROR: outer executor block not found")

text = text.replace(old_outer, new_outer, 1)

# The original block currently has no explicit shutdown after the
# as_completed loop. Add a non-blocking shutdown immediately before
# Phase 4.

anchor = '''                previous_results.append(
                    result
                )

        # ====================================================
        # PHASE 4
'''

replacement = '''                previous_results.append(
                    result
                )

        finally:
            # Never let executor shutdown become an implicit barrier.
            # Research results already collected remain valid.
            pool.shutdown(
                wait=False,
                cancel_futures=True
            )

        # ====================================================
        # PHASE 4
'''

if anchor not in text:
    raise SystemExit("ERROR: Phase 4 insertion anchor not found")

text = text.replace(anchor, replacement, 1)

P.write_text(text, encoding="utf-8")
py_compile.compile(str(P), doraise=True)

print("=" * 78)
print("IMA RESEARCH COUNCIL V5.5 — MEDA HANG HARDENING")
print("=" * 78)
print("BACKUP:", backup)
print("COMPILE: PASS")
print("OUTER EXECUTOR: NON-BLOCKING SHUTDOWN")
print("CANCEL PENDING FUTURES: PASS")
print("PATCH: PASS")
print("=" * 78)
