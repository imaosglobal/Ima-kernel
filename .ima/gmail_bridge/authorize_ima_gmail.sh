#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$(dirname "$0")/../.."
echo "[IMA] Starting permanent Gmail authorization..."
echo "[IMA] Required account: imaosglobal@gmail.com"
python -c 'import importlib.util; p=".ima/gmail_bridge/ima_gmail_build_watch.py"; s=importlib.util.spec_from_file_location("ima_gmail_watch",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); m.authorize(); print("[IMA] Gmail API authorization stored for imaosglobal@gmail.com")'
