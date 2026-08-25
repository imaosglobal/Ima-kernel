#!/bin/bash
echo "=== מועצת IMA - ישיבת חירום 25.08.2026 ===" > council_final_report.txt
echo "נושא: האם ניתן להפעיל עם כסף אמיתי?" >> council_final_report.txt
echo "" >> council_final_report.txt

echo "--- 1. ג'מיני: בדיקת תשתית ופרודקשן ---" >> council_final_report.txt
python3 ima_system.py audit --production-check >> council_final_report.txt 2>&1
echo "" >> council_final_report.txt

echo "--- 2. קלוד: בדיקת ארכיטקטורה ונקודות כשל ---" >> council_final_report.txt
./ima_architecture_audit.sh --full >> council_final_report.txt 2>&1
echo "" >> council_final_report.txt

echo "--- 3. מדה: בדיקת אבטחה וGO/NO-GO לכסף אמיתי ---" >> council_final_report.txt
./ima_product_readiness_audit.sh >> council_final_report.txt 2>&1
echo "" >> council_final_report.txt

echo "--- 4. שאלות ליושב ראש ---" >> council_final_report.txt
echo "א. האם אפשר להפעיל עם כסף אמיתי או רק סימולציה?" >> council_final_report.txt
echo "ב. מה חסר כדי לעבור לאמיתי?" >> council_final_report.txt
echo "ג. 3 צעדים לעשות מיד עכשיו" >> council_final_report.txt

cat council_final_report.txt
