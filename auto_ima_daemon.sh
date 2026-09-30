#!/data/data/com.termux/files/usr/bin/bash
while true; do
  python ~/Ima-kernel/founder/agents/sellers/auto_verifier.py >> ~/Ima-kernel/.ima/remote/auto.log 2>&1
  sleep 5
done
