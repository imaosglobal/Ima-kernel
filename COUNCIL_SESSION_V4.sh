#!/bin/bash
echo "========================================" > council_v4_report.txt
echo "IMA COUNCIL V4 - AUDIT FULL SYSTEM" >> council_v4_report.txt
echo "Date: $(date)" >> council_v4_report.txt
echo "========================================" >> council_v4_report.txt

echo "" >> council_v4_report.txt
echo "[1. CORE FILES]" >> council_v4_report.txt
ls -la .ima/ >> council_v4_report.txt
ls -la .ima_guardian/ >> council_v4_report.txt

echo "" >> council_v4_report.txt
echo "[2. SECURITY AUDIT]" >> council_v4_report.txt
grep -r "password\|secret\|key" . --include="*.py" --include="*.json" | grep -v ".git" >> council_v4_report.txt || echo "No hardcoded secrets found" >> council_v4_report.txt

echo "" >> council_v4_report.txt
echo "[3. CHILD SAFETY AUDIT]" >> council_v4_report.txt
find . -name "*child*" -type f >> council_v4_report.txt

echo "" >> council_v4_report.txt
echo "[4. VOICE + PERSONALITY]" >> council_v4_report.txt
cat .ima/personality.json 2>/dev/null || echo "personality.json MISSING" >> council_v4_report.txt
cat .ima/voice.json 2>/dev/null || echo "voice.json MISSING" >> council_v4_report.txt

echo "" >> council_v4_report.txt
echo "[5. BLOCKCHAIN READY]" >> council_v4_report.txt
ls -la deploy.js package.json >> council_v4_report.txt 2>/dev/null || echo "Blockchain files not found" >> council_v4_report.txt

echo "" >> council_v4_report.txt
echo "[6. ARCHIVE BACKUP CHECK]" >> council_v4_report.txt
ls _archive_20260808/ >> council_v4_report.txt

echo "" >> council_v4_report.txt
echo "=== COUNCIL VERDICT ===" >> council_v4_report.txt
echo "Files scanned: $(find . -type f | wc -l)" >> council_v4_report.txt
echo "Status: READY FOR TESTNET IF NO CRITICAL ERRORS" >> council_v4_report.txt

cat council_v4_report.txt
git add council_v4_report.txt && git commit -m "IMA v2.4.1: Council V4 Full Audit" && git push
