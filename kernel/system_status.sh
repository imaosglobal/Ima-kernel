echo "=== IMA STATUS ==="
echo "MODE: $(cat ~/ima_core/kernel/MODE)"
echo "SERVER: $(pgrep -f ima_pro_saas.js >/dev/null && echo RUNNING || echo DOWN)"
echo "LAST CHECK:"
tail -n 3 ~/ima_core/kernel/health.log
