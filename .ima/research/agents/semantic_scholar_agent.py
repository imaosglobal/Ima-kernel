from __future__ import annotations

import json
import time
import threading
import urllib.parse
import urllib.request
import urllib.error
from typing import Any


class SemanticScholarAgent:
    """
    Robust Semantic Scholar literature adapter for IMA Research Council V5.2.

    Contract:
        investigate(question) -> dict

    Never raises ordinary network/API failures to the council.
    Returns a structured ERROR result instead.
    """

    name = "SEMANTIC_SCHOLAR"

    API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

    DEFAULT_TIMEOUT = 20
    MAX_RETRIES = 4
    PAGE_SIZE = 8

    # Semantic Scholar rate-limit protection.
    _rate_lock = threading.Lock()
    _last_request_time = 0.0

    # Same-process cache prevents duplicate literature requests.
    _cache_lock = threading.Lock()
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

    FIELDS = ",".join([
        "paperId",
        "title",
        "abstract",
        "year",
        "authors",
        "venue",
        "url",
        "citationCount",
        "referenceCount",
    ])

    def __init__(self, timeout: int | None = None):
        self.timeout = int(timeout or self.DEFAULT_TIMEOUT)

    # ------------------------------------------------------------
    # PUBLIC CONTRACT
    # ------------------------------------------------------------

    def investigate(self, question: str) -> dict[str, Any]:
        started = time.time()

        question = str(question or "").strip()

        if not question:
            return self._error(
                "EMPTY_QUESTION",
                "Semantic Scholar received an empty question.",
                started,
            )

        try:
            papers = self._search(question)

            normalized = [
                self._normalize_paper(p)
                for p in papers
                if isinstance(p, dict)
            ]

            normalized = [
                p for p in normalized
                if p.get("title")
            ]

            answer = self._build_answer(
                question,
                normalized,
            )

            return {
                "agent": self.name,
                "status": "ANSWER_READY",
                "scientific_failure": False,
                "question": question,
                "answer": answer,
                "papers": normalized,
                "paper_count": len(normalized),
                "source": "Semantic Scholar",
                "api": self.API_URL,
                "duration": round(time.time() - started, 3),
            }

        except Exception as exc:
            # The council must receive a structured result,
            # not an uncaught exception from an external service.
            message = str(exc)

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

    # ------------------------------------------------------------
    # HTTP
    # ------------------------------------------------------------

    def _search(self, question: str) -> list[dict[str, Any]]:
        """
        Rate-limited, serialized Semantic Scholar request.

        Important:
        The Research Council executes agents concurrently.
        Semantic Scholar requests must NOT execute concurrently.
        """

        cache_key = " ".join(str(question).lower().split())

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

                    # Successful request closes/resets the breaker.
                    with self._circuit_lock:
                        self._consecutive_429 = 0
                        self._blocked_until = 0.0

                    # Cache successful results.
                    with self._cache_lock:
                        self._cache[cache_key] = list(data)

                    return data

                except urllib.error.HTTPError as exc:
                    last_error = exc

                    if exc.code == 429:

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

    # ------------------------------------------------------------
    # NORMALIZATION
    # ------------------------------------------------------------

    def _normalize_paper(
        self,
        paper: dict[str, Any],
    ) -> dict[str, Any]:

        authors = paper.get("authors") or []

        if isinstance(authors, list):
            author_names = [
                str(a.get("name", "")).strip()
                for a in authors
                if isinstance(a, dict)
            ]
            author_names = [
                a for a in author_names if a
            ]
        else:
            author_names = []

        abstract = paper.get("abstract")

        if abstract is not None:
            abstract = str(abstract).strip()

        return {
            "paper_id": paper.get("paperId"),
            "title": str(
                paper.get("title") or ""
            ).strip(),
            "abstract": abstract,
            "year": paper.get("year"),
            "authors": author_names,
            "venue": str(
                paper.get("venue") or ""
            ).strip(),
            "url": paper.get("url"),
            "citation_count": paper.get("citationCount", 0),
            "reference_count": paper.get("referenceCount", 0),
        }

    # ------------------------------------------------------------
    # SYNTHESIS
    # ------------------------------------------------------------

    def _build_answer(
        self,
        question: str,
        papers: list[dict[str, Any]],
    ) -> str:

        if not papers:
            return (
                "Semantic Scholar returned no papers for this query. "
                "No literature-based conclusion was inferred."
            )

        lines = [
            f"Semantic Scholar literature search for: {question}",
            "",
            f"Retrieved {len(papers)} candidate papers.",
            "",
        ]

        for index, paper in enumerate(papers, 1):
            title = paper.get("title") or "Untitled"
            year = paper.get("year") or "unknown year"
            venue = paper.get("venue") or "unknown venue"
            citations = paper.get("citation_count", 0)

            lines.append(
                f"{index}. {title} "
                f"({year}; {venue}; citations={citations})"
            )

            abstract = paper.get("abstract")

            if abstract:
                compact = " ".join(
                    str(abstract).split()
                )

                if len(compact) > 700:
                    compact = compact[:700] + "..."

                lines.append(
                    f"   Abstract: {compact}"
                )

        lines.extend([
            "",
            "Important: this retrieval layer reports literature evidence; "
            "it does not by itself establish the truth of the hypothesis.",
        ])

        return "\n".join(lines)

    # ------------------------------------------------------------
    # STRUCTURED ERROR
    # ------------------------------------------------------------

    def _error(
        self,
        error_type: str,
        message: str,
        started: float,
    ) -> dict[str, Any]:

        return {
            "agent": self.name,
            "status": "ERROR",
            "scientific_failure": False,
            "error_type": error_type,
            "error": message,
            "answer": None,
            "papers": [],
            "paper_count": 0,
            "duration": round(
                time.time() - started,
                3,
            ),
        }


# Compatibility helper
def investigate(question: str) -> dict[str, Any]:
    return SemanticScholarAgent().investigate(question)
