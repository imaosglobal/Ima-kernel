from __future__ import annotations

import json
import time
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
    MAX_RETRIES = 3
    PAGE_SIZE = 8

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
            return self._error(
                type(exc).__name__,
                str(exc),
                started,
            )

    # ------------------------------------------------------------
    # HTTP
    # ------------------------------------------------------------

    def _search(self, question: str) -> list[dict[str, Any]]:
        params = urllib.parse.urlencode({
            "query": question,
            "limit": self.PAGE_SIZE,
            "fields": self.FIELDS,
        })

        url = f"{self.API_URL}?{params}"

        last_error = None

        for attempt in range(self.MAX_RETRIES):
            try:
                request = urllib.request.Request(
                    url,
                    headers={
                        "Accept": "application/json",
                        "User-Agent": "IMA-Research-Council/5.2",
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
                        raw.decode("utf-8", errors="replace")
                    )

                if not isinstance(payload, dict):
                    raise RuntimeError(
                        "Semantic Scholar returned a non-object JSON response."
                    )

                data = payload.get("data", [])

                if data is None:
                    return []

                if not isinstance(data, list):
                    raise RuntimeError(
                        "Semantic Scholar response field 'data' is not a list."
                    )

                return data

            except urllib.error.HTTPError as exc:
                last_error = exc

                # Retry rate limiting and transient server failures.
                if exc.code == 429 or 500 <= exc.code < 600:
                    retry_after = exc.headers.get("Retry-After")

                    try:
                        delay = float(retry_after)
                    except (TypeError, ValueError):
                        delay = 2 ** attempt

                    # Never sleep excessively inside the research cycle.
                    time.sleep(min(delay, 8))
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
                TimeoutError,
            ) as exc:
                last_error = exc

                if attempt + 1 < self.MAX_RETRIES:
                    time.sleep(min(2 ** attempt, 4))
                    continue

                raise RuntimeError(
                    f"Semantic Scholar network failure: {exc}"
                ) from exc

            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    f"Semantic Scholar returned invalid JSON: {exc}"
                ) from exc

        raise RuntimeError(
            f"Semantic Scholar request failed after "
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
