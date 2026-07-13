#!/data/data/com.termux/files/usr/bin/bash

set -u

URL="https://ima-915m.onrender.com"
DATE=$(date +%Y%m%d_%H%M%S)

OUT=".ima/releases/render_activation/fast_diagnostic_$DATE"
mkdir -p "$OUT"

echo "=== RENDER FAST DIAGNOSTIC ==="

for PATH_TEST in "/" "/health" "/status" "/version"; do

    echo "Testing $URL$PATH_TEST"

    curl \
      --connect-timeout 5 \
      --max-time 15 \
      -sS \
      -w "\nHTTP_CODE:%{http_code}\nTIME:%{time_total}\n" \
      "$URL$PATH_TEST" \
      > "$OUT/$(echo $PATH_TEST | tr '/' '_').txt" \
      || echo "FAILED" >> "$OUT/$(echo $PATH_TEST | tr '/' '_').txt"

done


cat > "$OUT/RENDER_DIAGNOSTIC.json" <<EOF
{
 "service":"srv-d0r96hadbo4c73a4o910",
 "url":"$URL",
 "status":"CHECKED",
 "timestamp":"$DATE"
}
EOF

echo
echo "RESULTS:"
cat "$OUT"/*.txt

echo
echo "OUTPUT:"
echo "$OUT"

echo "=== RENDER FAST DIAGNOSTIC COMPLETE ==="

