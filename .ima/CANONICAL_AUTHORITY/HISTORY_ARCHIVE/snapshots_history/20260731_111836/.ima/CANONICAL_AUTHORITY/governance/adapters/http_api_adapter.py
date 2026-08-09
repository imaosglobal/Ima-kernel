from pathlib import Path
import importlib.util
import json
import subprocess
import time

_CONTRACT = (
    Path(__file__).resolve().parents[1]
    / "UNIVERSAL_ADAPTER_CONTRACT.py"
)

_spec = importlib.util.spec_from_file_location(
    "ima_universal_adapter_contract",
    _CONTRACT,
)

_contract = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_contract)

UniversalAdapter = _contract.UniversalAdapter


class HTTPAPIAdapter(UniversalAdapter):
    VERSION = "2.0"

    def discover(self):
        return {
            "type": "http_api",
            "status": "available",
            "version": self.VERSION,
            "transport": "curl",
        }

    def connect(self, config=None):
        return {
            "connected": True,
            "config": config or {},
            "version": self.VERSION,
        }

    def capabilities(self):
        return [
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "HEAD",
            "OPTIONS",
            "http_status",
            "response_headers",
            "json_parsing",
            "request_body",
            "timeout",
            "retry",
            "response_limit",
            "latency_metrics",
            "verification",
        ]

    def execute(self, action, payload=None):
        if not action or "url" not in action:
            return {
                "ok": False,
                "error": "url_required",
            }

        url = str(action["url"])
        method = str(
            action.get("method", "GET")
        ).upper()

        timeout = int(
            action.get("timeout", 10)
        )

        retries = max(
            0,
            int(action.get("retries", 0)),
        )

        response_limit = int(
            action.get("response_limit", 0)
        )

        headers = {
            str(k): str(v)
            for k, v in action.get(
                "headers", {}
            ).items()
        }

        body = action.get(
            "body",
            payload,
        )

        cmd = [
            "curl",
            "--doh-url",
            "https://cloudflare-dns.com/dns-query",
            "-4",
            "-L",
            "--silent",
            "--show-error",
            "--max-time",
            str(timeout),
            "-X",
            method,
            "-D",
            "-",
            "-w",
            "\n__IMA_HTTP_STATUS__:%{http_code}\n"
            "__IMA_TOTAL_TIME__:%{time_total}\n"
            "__IMA_SIZE_DOWNLOAD__:%{size_download}\n",
        ]

        for key, value in headers.items():
            cmd += [
                "-H",
                f"{key}: {value}",
            ]

        if (
            body is not None
            and method in {
                "POST",
                "PUT",
                "PATCH",
                "DELETE",
            }
        ):
            if isinstance(
                body,
                (dict, list),
            ):
                body = json.dumps(body)

            cmd += [
                "--data",
                str(body),
            ]

        cmd.append(url)

        last_result = None

        for attempt in range(
            retries + 1
        ):
            started = time.monotonic()

            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout + 5,
                )

                elapsed = (
                    time.monotonic()
                    - started
                )

                raw = (
                    result.stdout
                    or ""
                )

                marker = (
                    "__IMA_HTTP_STATUS__:"
                )

                marker_pos = raw.rfind(
                    marker
                )

                http_status = None
                latency = elapsed
                bytes_downloaded = None

                if marker_pos >= 0:
                    body_part = raw[
                        :marker_pos
                    ]

                    metadata = raw[
                        marker_pos:
                    ].splitlines()

                    for line in metadata:
                        if line.startswith(
                            "__IMA_HTTP_STATUS__:"
                        ):
                            http_status = int(
                                line.split(
                                    ":",
                                    1,
                                )[1]
                            )

                        elif line.startswith(
                            "__IMA_TOTAL_TIME__:"
                        ):
                            latency = float(
                                line.split(
                                    ":",
                                    1,
                                )[1]
                            )

                        elif line.startswith(
                            "__IMA_SIZE_DOWNLOAD__:"
                        ):
                            bytes_downloaded = int(
                                float(
                                    line.split(
                                        ":",
                                        1,
                                    )[1]
                                )
                            )
                else:
                    body_part = raw

                if (
                    response_limit > 0
                    and len(body_part)
                    > response_limit
                ):
                    body_part = (
                        body_part[
                            :response_limit
                        ]
                    )

                ok = (
                    result.returncode == 0
                    and http_status is not None
                    and 200 <= http_status < 400
                )

                return {
                    "ok": ok,
                    "status": result.returncode,
                    "http_status": http_status,
                    "method": method,
                    "url": url,
                    "body": body_part,
                    "latency": latency,
                    "bytes": bytes_downloaded,
                    "attempt": attempt + 1,
                    **(
                        {
                            "error": result.stderr
                        }
                        if result.returncode != 0
                        else {}
                    ),
                }

            except subprocess.TimeoutExpired as exc:
                last_result = {
                    "ok": False,
                    "error": "timeout",
                    "attempt": attempt + 1,
                    "detail": str(exc),
                }

            except Exception as exc:
                last_result = {
                    "ok": False,
                    "error": type(exc).__name__,
                    "attempt": attempt + 1,
                    "detail": str(exc),
                }

        return (
            last_result
            or {
                "ok": False,
                "error": "request_failed",
            }
        )

    def observe(self):
        return {
            "adapter": "http_api",
            "status": "ready",
            "version": self.VERSION,
            "capabilities": self.capabilities(),
        }

    def verify(self, result):
        if not isinstance(
            result,
            dict,
        ):
            return False

        if result.get(
            "ok"
        ) is not True:
            return False

        status = result.get(
            "http_status"
        )

        return (
            isinstance(
                status,
                int,
            )
            and 200 <= status < 400
        )

    def disconnect(self):
        return {
            "connected": False,
            "version": self.VERSION,
        }
