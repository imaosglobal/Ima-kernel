#!/system/bin/sh
set -u
IN="/data/data/com.termux/files/home/.ima_bridge/in_$$"
OUT="/data/data/com.termux/files/home/.ima_bridge/out_$$"
cleanup() {
  /system/bin/toybox kill "${ADB_PID:-0}" 2>/dev/null || true
  /system/bin/toybox rm -f "$IN" "$OUT" 2>/dev/null || true
}
trap cleanup EXIT INT TERM
/system/bin/toybox mkfifo "$IN" "$OUT" || exit 1
/system/bin/nc 127.0.0.1 5037 <"$IN" >"$OUT" 2>/dev/null &
ADB_PID=$!
exec 3>"$IN"
exec 4<"$OUT"
/system/bin/toybox printf '%s' '0018host:transport-any' >&3
S1=$(/system/bin/toybox dd bs=4 count=1 <&4 2>/dev/null)
[ "$S1" = "OKAY" ] || exit 2
/system/bin/toybox printf '%s' '0024localabstract:chrome_devtools_remote' >&3
S2=$(/system/bin/toybox dd bs=4 count=1 <&4 2>/dev/null)
[ "$S2" = "OKAY" ] || exit 3
/system/bin/toybox cat <&0 >&3 &
P1=$!
/system/bin/toybox cat <&4 >&1 &
P2=$!
wait "$P1" 2>/dev/null || true
/system/bin/toybox kill "$P2" 2>/dev/null || true
