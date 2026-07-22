#!/data/data/com.termux/files/usr/bin/bash

echo "=== IMA PROVIDER CHECK ==="

echo ""
echo "[SYSTEM]"
uname -a

echo ""
echo "[NODE]"
node -v

echo ""
echo "[PYTHON]"
python --version

echo ""
echo "[DOCKER]"
docker --version 2>/dev/null || echo "docker unavailable"

echo ""
echo "[ENV]"
if [ -f .env.production ]; then
  echo ".env.production exists"
else
  echo ".env.production missing"
fi

echo ""
echo "=== DONE ==="
