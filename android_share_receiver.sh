#!/data/data/com.termux/files/usr/bin/bash

echo "=== IMA ANDROID SHARE RECEIVER ==="

if [ -n "$1" ]; then
    printf '%s\n' "$1" > .ima/shared_from_android.txt
    echo "RECEIVED: $1"
else
    echo "NO_TEXT_RECEIVED"
fi
