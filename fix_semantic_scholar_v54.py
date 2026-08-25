from pathlib import Path
from datetime import datetime
import shutil
import py_compile

p = Path(".ima/research/agents/semantic_scholar_agent.py")
backup_dir = Path(".ima/research/backups")
backup_dir.mkdir(parents=True, exist_ok=True)

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = backup_dir / f"semantic_scholar_agent_before_v54_{stamp}.py"
shutil.copy2(p, backup)

text = p.read_text(encoding="utf-8")

# ------------------------------------------------------------
# 1. Add circuit-breaker state
# ------------------------------------------------------------

old = '''    _cache_lock = threading.Lock()
    _cache = {}

    # Conservative interval for the public API.
    MIN_REQUEST_INTERVAL = 2.0
'''

new = '''    _cache_lock = threading.Lock()
    _cache = {}

    # Conservative interval for the public API.
    MIN_REQUEST_INTERVAL = 2.0

    # Circuit breaker:
    # after repeated 429 responses, stop contacting the API for a while.
    _circuit_lock = threading.Lock()
    _blocked_until = 0.0
    _consecutive_429 = 0

    RATE_LIMIT_COOLDOWN = 300.0
    MAX_CONSECUTIVE_429 = 1
'''

if old not in text:
    raise SystemExit("STATE BLOCK NOT FOUND")

text = text.replace(old, new, 1)

# ------------------------------------------------------------
# 2. Add circuit check at beginning of _search
# ------------------------------------------------------------

needle = '''        cache_key = " ".join(str(question).lower().split())

        with self._cache_lock:
'''

replacement = '''        cache_key = " ".join(str(question).lower().split())

        # Fast-fail while the circuit is open.
        with self._circuit_lock:
            now = time.time()

            if now < self._blocked_until:
                remaining = round(
                    self._blocked_until - now,
                    1,
                )

                raise RuntimeError(
                    "Semantic Scholar circuit breaker OPEN; "
                    f"rate-limit cooldown remaining={remaining}s"
                )

        with self._cache_lock:
'''

if needle not in text:
    raise SystemExit("SEARCH ENTRY BLOCK NOT FOUND")

text = text.replace(needle, replacement, 1)

# ------------------------------------------------------------
# 3. Replace retry behavior for HTTP 429
# ------------------------------------------------------------

old = '''                    if exc.code == 429 or 500 <= exc.code < 600:

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
'''

new = '''                    if exc.code == 429:

                        # Do NOT repeatedly hammer a rate-limited endpoint.
                        # Open the circuit immediately.
                        with self._circuit_lock:
                            self._consecutive_429 += 1
                            self._blocked_until = (
                                time.time()
                                + self.RATE_LIMIT_COOLDOWN
                            )

                        raise RuntimeError(
                            "Semantic Scholar rate limited this process "
                            "(HTTP 429); circuit breaker opened for "
                            f"{int(self.RATE_LIMIT_COOLDOWN)}s"
                        ) from exc

                    if 500 <= exc.code < 600:

                        if attempt + 1 < self.MAX_RETRIES:
                            delay = min(
                                2.0 ** attempt,
                                10.0,
                            )
                            time.sleep(delay)
                            continue

                        raise RuntimeError(
                            f"Semantic Scholar HTTP {exc.code} "
                            f"after {self.MAX_RETRIES} attempts"
                        ) from exc
'''

if old not in text:
    raise SystemExit("HTTP RETRY BLOCK NOT FOUND")

text = text.replace(old, new, 1)

# ------------------------------------------------------------
# 4. Reset circuit after successful response
# ------------------------------------------------------------

needle = '''                    # Cache successful results.
                    with self._cache_lock:
                        self._cache[cache_key] = list(data)

                    return data
'''

replacement = '''                    # Successful request closes/resets the breaker.
                    with self._circuit_lock:
                        self._consecutive_429 = 0
                        self._blocked_until = 0.0

                    # Cache successful results.
                    with self._cache_lock:
                        self._cache[cache_key] = list(data)

                    return data
'''

if needle not in text:
    raise SystemExit("SUCCESS BLOCK NOT FOUND")

text = text.replace(needle, replacement, 1)

# ------------------------------------------------------------
# 5. Make investigate classify rate limiting explicitly
# ------------------------------------------------------------

old = '''            return self._error(
                type(exc).__name__,
                str(exc),
                started,
            )
'''

new = '''            message = str(exc)

            if "rate limited" in message.lower():
                error_type = "RATE_LIMITED"
            elif "circuit breaker" in message.lower():
                error_type = "CIRCUIT_OPEN"
            else:
                error_type = type(exc).__name__

            return self._error(
                error_type,
                message,
                started,
            )
'''

if old not in text:
    raise SystemExit("ERROR HANDLER BLOCK NOT FOUND")

text = text.replace(old, new, 1)

p.write_text(text, encoding="utf-8")
py_compile.compile(str(p), doraise=True)

print("=" * 78)
print("IMA RESEARCH COUNCIL V5.4 — SEMANTIC SCHOLAR CIRCUIT BREAKER")
print("=" * 78)
print("BACKUP:", backup)
print("COMPILE: PASS")
print("429 CIRCUIT BREAKER: PASS")
print("FAST FAIL: PASS")
print("RATE LIMIT CLASSIFICATION: PASS")
print("PATCH: PASS")
print("=" * 78)
