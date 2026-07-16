#!/data/data/com.termux/files/usr/bin/bash

echo "=== IMA GAP SCAN ==="

check(){
    if [ -e "$1" ]; then
        echo "[FOUND] $1"
    else
        echo "[MISS ] $1"
    fi
}

echo ""
echo "[IDENTITY]"
check "IMA_START.py"
check "ima_master_runtime.py"
check "conversation_layer.py"

echo ""
echo "[MEMORY]"
find . -iname "*memory*" | head -10

echo ""
echo "[PERSONA]"
find . -iname "*persona*" -o -iname "*identity*" -o -iname "*character*" | head -10

echo ""
echo "[LEARNING]"
find . -iname "*learning*" -o -iname "*knowledge*" -o -iname "*world*" | head -10

echo ""
echo "[CONNECTORS]"
find . -iname "*api*" -o -iname "*bridge*" -o -iname "*connector*" -o -iname "*plugin*" | head -15

echo ""
echo "[UI / AVATAR]"
find . -iname "*avatar*" -o -iname "*3d*" -o -iname "*ui*" -o -iname "*frontend*" | head -15

echo ""
echo "[LANGUAGES]"
find . -iname "*language*" -o -iname "*locale*" -o -iname "*i18n*" -o -iname "*translation*" | head -15

echo ""
echo "[AUTONOMY]"
find . -iname "*agent*" -o -iname "*self*" -o -iname "*heal*" -o -iname "*evolution*" | head -15

echo ""
echo "=== END ==="
