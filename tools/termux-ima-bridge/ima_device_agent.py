#!/usr/bin/env python3
"""IMA Universal Device Agent: outbound-only owner-scoped command executor."""

import json
import os
import pathlib
import time
import urllib.error
import urllib.request

API = os.environ.get("IMA_DEVICE_API", "https://ima-915m.onrender.com").rstrip("/")
KEY_FILE = pathlib.Path(os.environ.get("IMA_DEVICE_KEY_FILE", "~/.ima-device-key")).expanduser()
DOWNLOADS = pathlib.Path(os.environ.get("IMA_ANDROID_DOWNLOADS", "~/storage/downloads")).expanduser()
LOCAL_BRIDGE = os.environ.get("IMA_LOCAL_BRIDGE", "http://127.0.0.1:8787").rstrip("/")
POLL_SECONDS = max(1, float(os.environ.get("IMA_DEVICE_POLL_SECONDS", "3")))
RESULT_TIMEOUT = max(3, float(os.environ.get("IMA_ANDROID_RESULT_TIMEOUT", "20")))

def load_key():
    value = os.environ.get("IMA_DEVICE_KEY", "").strip()
    if value:
        return value
    if KEY_FILE.exists():
        return KEY_FILE.read_text(encoding="utf-8").strip()
    raise RuntimeError("IMA device key is missing")

def api(method, path, payload=None):
    key = load_key()
    body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode()
    headers = {"X-IMA-Device-Key": key, "Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(API + path, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=35) as response:
        if response.status == 204:
            return None
        raw = response.read()
        return json.loads(raw.decode("utf-8")) if raw else {}

def local(method, path, payload=None):
    body = None if payload is None else json.dumps(payload).encode()
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(LOCAL_BRIDGE + path, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=8) as response:
        return json.loads(response.read().decode("utf-8"))

def write_android_command(command):
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    command_path = DOWNLOADS / "ima_remote_command.json"
    result_path = DOWNLOADS / "ima_remote_result.json"
    result_path.unlink(missing_ok=True)
    command_path.write_text(json.dumps(command, ensure_ascii=False), encoding="utf-8")
    deadline = time.time() + RESULT_TIMEOUT
    while time.time() < deadline:
        if result_path.exists():
            try:
                data = json.loads(result_path.read_text(encoding="utf-8"))
                result_path.unlink(missing_ok=True)
                command_path.unlink(missing_ok=True)
                return data
            except (OSError, ValueError):
                pass
        time.sleep(0.25)
    command_path.unlink(missing_ok=True)
    raise TimeoutError("Android accessibility command timed out")

def execute(command):
    action = command.get("action")
    payload = command.get("payload") or {}
    if action == "status":
        return local("GET", "/status")
    if action == "screenshot":
        return local("GET", "/screenshot")
    if action == "tabs":
        return local("GET", "/tabs")
    if action == "navigate":
        return local("POST", "/navigate", {"url": payload.get("url", "")})
    if action == "click":
        return local("POST", "/click", {"selector": payload.get("selector", "")})
    if action == "type":
        return local("POST", "/type", {"text": payload.get("text", "")})
    if action == "key":
        return local("POST", "/key", {"key": payload.get("key", "")})
    if action.startswith("android_"):
        native_action = action.removeprefix("android_")
        return write_android_command({"id": command.get("id"), "action": native_action, **payload})
    raise ValueError("unsupported device action")

def main():
    print("IMA universal device agent online", flush=True)
    while True:
        try:
            response = api("GET", "/ima-api/device/poll")
            if response and response.get("command"):
                command = response["command"]
                try:
                    result = execute(command)
                    api("POST", "/ima-api/device/result", {
                        "command_id": command["id"], "ok": True, "result": result
                    })
                except Exception as exc:
                    api("POST", "/ima-api/device/result", {
                        "command_id": command["id"], "ok": False, "error": str(exc)[:1000]
                    })
        except urllib.error.HTTPError as exc:
            if exc.code == 401:
                print("IMA device authentication failed; check the device key.", flush=True)
                time.sleep(15)
            else:
                time.sleep(5)
        except Exception:
            time.sleep(5)
        time.sleep(POLL_SECONDS)

if __name__ == "__main__":
    main()
