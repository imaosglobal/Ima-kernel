#!/data/data/com.termux/files/usr/bin/bash

echo "================================"
echo "IMA EXPERIENCE AUDIT"
echo "================================"

echo
echo "=== UI STRUCTURE ==="
find ima-ui -maxdepth 3 -type d | sort

echo
echo "=== UI COMPONENTS ==="
find ima-ui/src -type f | sort

echo
echo "=== 3D / XR / VISUAL SEARCH ==="
find . -iname "*3d*" \
-o -iname "*three*" \
-o -iname "*avatar*" \
-o -iname "*vr*" \
-o -iname "*ar*" \
-o -iname "*xr*" \
-o -iname "*model*" \
| head -100

echo
echo "=== ROBOTICS / DEVICE LAYER ==="
find . -iname "*robot*" \
-o -iname "*iot*" \
-o -iname "*bluetooth*" \
-o -iname "*sensor*" \
-o -iname "*device*" \
| head -100

echo
echo "=== AI / LEARNING LAYERS ==="
find . -iname "*learn*" \
-o -iname "*agent*" \
-o -iname "*brain*" \
-o -iname "*knowledge*" \
-o -iname "*memory*" \
| head -100

echo
echo "=== PACKAGE DEPENDENCIES ==="
cat ima-ui/package.json

echo
echo "=== COMPLETE ==="
