from flask import Flask, request, Response, send_from_directory
import json, os
import ima_master_runtime

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route("/ima", methods=["POST"])
def ima_endpoint():
    data = request.json
    text = data.get("text", "")
    sender = data.get("sender", "guest")
    parts = text.split()
    if not parts: reply = "מה?"
    else:
        cmd = parts[0]
        if cmd == "חפש": reply = ima_master_runtime.ima_profile.ima_search(" ".join(parts[1:]), sender)
        elif cmd == "תהיי": reply = ima_master_runtime.ima_profile.request_form_change(sender, parts[1])
        elif cmd == "דודל": d = ima_master_runtime.ima_profile.get_today_doodle(); reply = f"הדודל של היום: {d['form']} | סיבה: {d['reason']}"
        else: reply = "פקודות: חפש [מילה] | תהיי [צורה] | דודל"
    return Response(json.dumps({"reply": reply}, ensure_ascii=False), mimetype='application/json; charset=utf-8')

@app.route("/ima/design", methods=["GET"])
def get_design():
    trend = ima_master_runtime.ima_profile.get_design_for_today()
    return Response(json.dumps(trend, ensure_ascii=False), mimetype='application/json; charset=utf-8')

@app.route("/")
def serve_index():
    return send_from_directory('.', 'index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False, use_reloader=False)
