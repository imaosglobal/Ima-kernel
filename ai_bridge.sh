#!/data/data/com.termux/files/usr/bin/bash

CMD="$1"

curl -s -X POST http://127.0.0.1:7777 \
 -d "{\"cmd\":\"$CMD\"}"

