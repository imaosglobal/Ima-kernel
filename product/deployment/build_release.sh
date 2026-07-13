#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_kernel

echo "=== BUILD IMA RELEASE ==="

python3 -m product.deployment.deployment_manager

echo "=== RELEASE MANIFEST CREATED ==="
