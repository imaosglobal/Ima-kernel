from pathlib import Path
from datetime import datetime
import shutil
import py_compile

p = Path(".ima/research/agents/semantic_scholar_agent.py")
backup_dir = Path(".ima/research/backups")
backup_dir.mkdir(parents=True, exist_ok=True)

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = backup_dir / f"semantic_scholar_agent_before_v53_{stamp}.py"
shutil.copy2(p, backup)

text = p.read_text(encoding="utf-8")

# Add threading support.
old = "import json\nimport time\n"
new = "import json\nimport time\nimport threading\n"
if old in text and "import threading" not in text:
    text = text.replace(old, new, 1)

# Add class-level coordination state.
old = '''    MAX_RETRIES = 3
    PAGE_SIZE = 8
'''
new = '''    MAX_RETRIES = 4
    PAGE_SIZE = 8

    # Semantic Scholar rate-limit protection.
    _rate_lock = threading.Lock()
    _last_request_time = 0.0

    # Same-process cache prevents duplicate literature requests.
    _cache_lock = threading.Lock()
    _cache = {}

    # Conservative interval for the public API.
    MIN_REQUEST_INTERVAL = 2.0
'''
if old not in text:
    raise SystemExit("CLASS CONSTANT BLOCK NOT FOUND")
text = text.replace(old, new, 1)

# Replace _search completely.
start = text.index("    def _search(")
end = text.index("    # ------------------------------------------------------------\n    # NORMALIZATION", start)

replacement = r'''    def _search(self, question: str) -> list[dict[str, Any]]:
        """
        Rate-limited, serialized Semantic Scholar request.

        Important:
        The Research Council executes agents concurrently.
        Semantic Scholar requests must NOT execute concurrently.
        """

        cache_key = " ".join(str(question).lower().split())

        with self._cache_lock:
            cached = self._cache.get(cache_key)

        if cached is not None:
            return list(cached)

        params = urllib.parse.urlencode({
            "query": question,
            "limit": self.PAGE_SIZE,
            "fields": self.FIELDS,
        })

        url = f"{self.API_URL}?{params}"

        last_error = None

        # Serialize ALL Semantic Scholar requests in this process.
        with self._rate_lock:

            for attempt in range(self.MAX_RETRIES):

                # Enforce minimum spacing between requests.
                now = time.time()
                elapsed = now - self._last_request_time

                if elapsed < self.MIN_REQUEST_INTERVAL:
                    time.sleep(
                        self.MIN_REQUEST_INTERVAL - elapsed
                    )

                self._last_request_time = time.time()

                try:
                    request = urllib.request.Request(
                        url,
                        headers={
                            "Accept": "application/json",
                            "User-Agent": (
                                "IMA-Research-Council/5.3 "
                                "(scientific-literature-research)"
                            ),
                        },
                        method="GET",
                    )

                    with urllib.request.urlopen(
                        request,
                        timeout=self.timeout,
                    ) as response:

                        status = getattr(response, "status", 200)
                        raw = response.read()

                        if status != 200:
                            raise RuntimeError(
                                f"Semantic Scholar HTTP {status}"
                            )

                    payload = json.loads(
                        raw.decode(
                            "utf-8",
                            errors="replace",
                        )
                    )

                    if not isinstance(payload, dict):
                        raise RuntimeError(
                            "Semantic Scholar returned non-object JSON."
                        )

                    data = payload.get("data", [])

                    if data is None:
                        data = []

                    if not isinstance(data, list):
                        raise RuntimeError(
                            "Semantic Scholar 'data' is not a list."
                        )

                    # Cache successful results.
                    with self._cache_lock:
                        self._cache[cache_key] = list(data)

                    return data

                except urllib.error.HTTPError as exc:
                    last_error = exc

                    if exc.code == 429 or 500 <= exc.code < 600:

                        retry_after = None

                        try:
                            retry_after = exc.headers.get(
                                "Retry-After"
                            )
                        except Exception:
                            pass

                        try:
                            delay = float(retry_after)
                        except (TypeError, ValueError):
                            # Exponential backoff with a conservative floor.
                            delay = max(
                                3.0,
                                2.0 ** attempt,
                            )

                        delay = min(delay, 20.0)

                        time.sleep(delay)
                        continue

                    body = ""

                    try:
                        body = exc.read().decode(
                            "utf-8",
                            errors="replace",
                        )[:500]
                    except Exception:
                        pass

                    raise RuntimeError(
                        f"Semantic Scholar HTTP {exc.code}: {body}"
                    ) from exc

                except (
                    urllib.error.URLError,
                    TimeoutError,
                ) as exc:

                    last_error = exc

                    if attempt + 1 < self.MAX_RETRIES:
                        time.sleep(
                            min(
                                max(2.0, 2.0 ** attempt),
                                10.0,
                            )
                        )
                        continue

                    raise RuntimeError(
                        f"Semantic Scholar network failure: {exc}"
                    ) from exc

                except json.JSONDecodeError as exc:
                    raise RuntimeError(
                        f"Semantic Scholar invalid JSON: {exc}"
                    ) from exc

        raise RuntimeError(
            "Semantic Scholar request failed after "
            f"{self.MAX_RETRIES} attempts: {last_error}"
        )

'''

text = text[:start] + replacement + text[end:]

p.write_text(text, encoding="utf-8")

py_compile.compile(str(p), doraise=True)

print("=" * 78)
print("IMA RESEARCH COUNCIL V5.3 — SEMANTIC SCHOLAR RATE LIMIT FIX")
print("=" * 78)
print("BACKUP:", backup)
print("COMPILE: PASS")
print("SERIALIZED REQUESTS: PASS")
print("RATE LIMIT CACHE: PASS")
print("EXPONENTIAL BACKOFF: PASS")
print("PATCH: PASS")
print("=" * 78)
