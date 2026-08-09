import sys
import json

sys.path.insert(0, "/data/data/com.termux/files/home/ima_kernel")

from connectors.whatsapp.whatsapp_connector import whatsapp

if len(sys.argv) < 2:
    print("אין הודעה")
    exit()

text = sys.argv[1]

reply = whatsapp.receive_message(
    "whatsapp_user",
    text
)

print(reply)
