#!/data/data/com.termux/files/usr/bin/bash
cd ~/ima_kernel
pkill -f ima_server.py
echo "מרים את IMA עם Auto-Restart..."
while true; do
    python ima_server.py
    echo "IMA נפלה. מריץ מחדש בעוד 3 שניות..."
    sleep 3
done
