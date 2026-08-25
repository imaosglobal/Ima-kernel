#!/bin/bash
cd /data/data/com.termux/files/home/Ima-kernel
echo "=== מועצת IMA - ישיבת שיפורים 25.08.2026 ===" > council_improvements_report.txt
echo "נושא: בדיקת כל המערכת + הצעות שיפור לפני TESTNET" >> council_improvements_report.txt
echo "" >> council_improvements_report.txt
echo "--- 1. ג'מיני: פרודקשן + ביצועים ---" >> council_improvements_report.txt
python3 ima_system.py audit --production-check --performance >> council_improvements_report.txt 2>&1
echo "" >> council_improvements_report.txt
echo "--- 2. קלוד: ארכיטקטורה + חובות טכניים ---" >> council_improvements_report.txt
./ima_architecture_audit.sh --full --suggest-improvements >> council_improvements_report.txt 2>&1
echo "" >> council_improvements_report.txt
echo "--- 3. מדה: אבטחה + GO/NO-GO לTESTNET ---" >> council_improvements_report.txt
./ima_product_readiness_audit.sh --testnet-ready >> council_improvements_report.txt 2>&1
cat council_improvements_report.txt
