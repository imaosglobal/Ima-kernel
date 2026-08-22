from pathlib import Path
import subprocess

# audit עמוק רק לפי צורך
if not Path("IMA_AUDIT_REPORT.json").exists():
    subprocess.run(["python3","ima_full_audit.py"])

else:
