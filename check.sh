#!/bin/bash
echo "=== Dead code check ==="
vulture ~/ima_kernel/*.py --min-confidence 80
echo ""
echo "=== Health check ==="
curl -s http://127.0.0.1:5001/health && echo "" || echo "SERVER NOT RESPONDING"
