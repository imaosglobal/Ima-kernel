#!/data/data/com.termux/files/usr/bin/bash
# IMA MASTER - מפעיל הכל
echo "💎 Starting IMA Empire Master..."

# 1. V4 Engine
if [! -f ~/Ima-kernel/.ima/muse_daemon.pid ]; then
  nohup python ~/Ima-kernel/muse_daemon_v4.py > /dev/null 2>&1 &
  echo $! > ~/Ima-kernel/.ima/muse_daemon.pid
  echo "✅ V4 Engine started PID $(cat ~/Ima-kernel/.ima/muse_daemon.pid)"
else
  echo "✅ V4 already running"
fi

# 2. Auto Verifier (בודק ומוכר)
if [! -f ~/Ima-kernel/.ima/auto_verifier.pid ]; then
  nohup bash ~/Ima-kernel/auto_ima_daemon.sh > /dev/null 2>&1 &
  echo $! > ~/Ima-kernel/.ima/auto_verifier.pid
  echo "✅ Auto-Verifier started PID $(cat ~/Ima-kernel/.ima/auto_verifier.pid)"
else
  echo "✅ Verifier already running"
fi

# 3. Auto Hunter (מוצא לידים)
if [! -f ~/Ima-kernel/.ima/hunter.pid ]; then
  nohup python ~/Ima-kernel/founder/agents/sellers/auto_lead_hunter.py > ~/Ima-kernel/.ima/remote/hunter.log 2>&1 &
  echo $! > ~/Ima-kernel/.ima/hunter.pid
  echo "✅ Auto-Hunter started PID $(cat ~/Ima-kernel/.ima/hunter.pid)"
else
  echo "✅ Hunter already running"
fi

echo ""
echo "💰 IMA MONEY MACHINE IS RUNNING!"
ps | grep -E "muse|hunter|verifier" | grep -v grep
