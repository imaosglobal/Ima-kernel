#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== FIX IMA SERVER ==="

cp api/server.py api/server.py.broken_backup

python3 <<'PY'
from pathlib import Path

p=Path("api/server.py")
s=p.read_text(encoding="utf-8")

start=s.find("    def do_POST(self):")
end=s.find("PORT=int", start)

new=r'''    def do_POST(self):
        try:
            if self.path == "/ask":

                size = int(self.headers.get("Content-Length",0))
                raw = self.rfile.read(size)
                data = json.loads(raw)

                question = data.get("message") or data.get("question","")

                answer = product_gateway.ask(question)

                try:
                    clean = route(question)
                    if clean:
                        answer = {
                            "response": clean,
                            "status": "OK"
                        }
                except Exception:
                    pass

                conversation_layer.update(question)

                self.send_json({
                    "input": question,
                    "answer": answer,
                    "time": int(time.time()),
                    "status": "OK"
                })

            else:
                self.send_json({
                    "error":"unknown endpoint",
                    "path":self.path
                })

        except Exception as e:
            self.send_json({
                "status":"ERROR",
                "error":str(e)
            })

'''

if start == -1 or end == -1:
    raise SystemExit("Could not locate server section")

s=s[:start]+new+s[end:]

p.write_text(s,encoding="utf-8")

PY

echo "=== TEST SYNTAX ==="

python3 -m py_compile api/server.py

echo "=== DONE ==="
