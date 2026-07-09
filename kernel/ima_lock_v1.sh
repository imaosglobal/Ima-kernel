
#!/data/data/com.termux/files/usr/bin/bash

echo "[LOCK v1] applying stabilization..."

# 1. הסרת רעשי snapshot echo
find ~/ima_core/kernel/snapshots -type f -name "bashrc_*" -exec sed -i '/ima:/d' {} \;

# 2. מניעת כפילויות CLI echo (אם קיימות)
grep -R "ima: restart | update | brain | health | queue" ~/ima_core/kernel/snapshots >/dev/null 2>&1
if [ $? -eq 0 ]; then
  find ~/ima_core/kernel/snapshots -type f -exec sed -i '/ima: restart | update | brain | health | queue/d' {} \;
fi

# 3. ייצוב daemon lock
mkdir -p ~/ima_core/kernel/runtime
echo "$(pgrep -f control_daemon.js || echo 0)" > ~/ima_core/kernel/runtime/daemon.lock

# 4. ניקוי רעשי runtime ישנים
rm -f ~/ima_core/kernel/*.tmp 2>/dev/null

echo "[LOCK v1] COMPLETE - SYSTEM STABILIZED"

