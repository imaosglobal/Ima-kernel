from pathlib import Path

p=Path("ima_guardian_controller.py")
text=p.read_text(encoding="utf8")

text=text.replace(
    'run("python3 ima_full_audit.py")',
    'run("python3 ima_guardian_report_scan.py")'
)

p.write_text(text,encoding="utf8")

Path("ima_guardian_report_scan.py").write_text(
'''from pathlib import Path
import subprocess

# audit עמוק רק לפי צורך
if not Path("IMA_AUDIT_REPORT.json").exists():
    subprocess.run(["python3","ima_full_audit.py"])

else:
''',
encoding="utf8"
)

