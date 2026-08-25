from pathlib import Path
import py_compile
import shutil
from datetime import datetime

P = Path(".ima/research/ima_research_council.py")

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = P.parent / "backups" / (
    f"ima_research_council_before_executor_v55_{stamp}.py"
)
backup.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(P, backup)

lines = P.read_text(encoding="utf-8").splitlines()

# Find the exact PHASE 3 executor block.
start = None
end = None

for i, line in enumerate(lines):
    if "with ThreadPoolExecutor(" in line:
        # Verify this is the PHASE 3 executor.
        window = "\n".join(lines[i:min(i + 15, len(lines))])
        if "futures = {}" in window:
            start = i
            break

if start is None:
    raise SystemExit("ERROR: PHASE 3 ThreadPoolExecutor not found")

# Find the end immediately before PHASE 4.
for i in range(start, len(lines)):
    if "PHASE 4" in lines[i]:
        end = i
        break

if end is None:
    raise SystemExit("ERROR: PHASE 4 boundary not found")

block = lines[start:end]

print("FOUND EXECUTOR BLOCK:")
print(f"  start line: {start + 1}")
print(f"  end line:   {end}")
print(f"  lines:      {len(block)}")

# The existing structure is:
#
# with ThreadPoolExecutor(...) as pool:
#     futures = {}
#     ...
#     for future ...
#         ...
#
# Replace the `with` line and remove exactly one indentation
# level from the body.

if not block[0].lstrip().startswith("with ThreadPoolExecutor("):
    raise SystemExit("ERROR: unexpected executor block structure")

# Locate the line that closes the constructor.
constructor_end = None
for j in range(len(block)):
    if block[j].strip() == ") as pool:":
        constructor_end = j
        break

if constructor_end is None:
    raise SystemExit("ERROR: executor constructor terminator not found")

new_block = [
    "        pool = ThreadPoolExecutor(",
    "            max_workers=max(",
    "                1,",
    "                len(jobs)",
    "            )",
    "        )",
    "",
]

# Everything after `) as pool:` belongs to the with-body.
body = block[constructor_end + 1:]

for line in body:
    if line.startswith("    "):
        new_block.append(line[4:])
    elif line.strip() == "":
        new_block.append(line)
    else:
        raise SystemExit(
            "ERROR: unexpected non-indented line inside executor body: "
            + repr(line)
        )

# Add explicit non-blocking shutdown before PHASE 4.
new_block.extend([
    "",
    "        # V5.5: do not use `with ThreadPoolExecutor` here.",
    "        # Its implicit __exit__ performs shutdown(wait=True),",
    "        # which can block the Council behind a slow MEDA worker.",
    "        pool.shutdown(",
    "            wait=False,",
    "            cancel_futures=True",
    "        )",
    "",
])

lines[start:end] = new_block

P.write_text("\n".join(lines) + "\n", encoding="utf-8")
py_compile.compile(str(P), doraise=True)

print("=" * 78)
print("IMA RESEARCH COUNCIL V5.5 — EXECUTOR HARDENING")
print("=" * 78)
print("BACKUP:", backup)
print("EXECUTOR BLOCK:", f"{start + 1}-{end}")
print("IMPLICIT WAIT=TRUE REMOVED: PASS")
print("NON-BLOCKING SHUTDOWN: PASS")
print("CANCEL FUTURES: PASS")
print("COMPILE: PASS")
print("PATCH: PASS")
print("=" * 78)
