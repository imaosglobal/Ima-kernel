import json
import re
import time
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError


class LiteratureAgent:

    name = "LITERATURE"

    def __init__(self, root=None):
        self.root = root

    # ---------------------------------------------------------
    # Query construction
    # ---------------------------------------------------------

    def _normalize_query(self, question):

        q = str(question).strip()

        # Remove generic research-council wording.
        replacements = [
            "What observations or measurements can actually bear on the question?",
            "What observations or experiments could distinguish the competing hypotheses?",
            "What remains genuinely unknown?",
            "What competing explanations exist?",
            "What mechanisms could explain the observed phenomenon without assuming the conclusion?",
        ]

        for item in replacements:
            q = q.replace(item, " ")

        q = re.sub(r"\s+", " ", q).strip()

        # Keep semantic content instead of generic meta-language.
        generic = {
            "בדיקת אינטגרציה",
            "בדיקת מערכת",
            "מה ההבדל בין",
            "מה נשאר לא ידוע",
            "מה ניתן למדוד",
            "מה ניתן לראות",
        }

        for word in generic:
            q = q.replace(word, " ")

        q = re.sub(r"\s+", " ", q).strip()

        if not q:
            q = str(question).strip()

        return q[:500]

    # ---------------------------------------------------------
    # Token relevance
    # ---------------------------------------------------------

    def _tokens(self, text):

        words = re.findall(
            r"[A-Za-zÀ-ÿ\u0590-\u05FF0-9]{3,}",
            str(text).lower()
        )

        stop = {
            "what", "which", "could", "would", "does", "that",
            "this", "from", "with", "without", "question",
            "observations", "measurements", "experiments",
            "remain", "genuinely", "unknown", "exist",
            "the", "and", "for", "are", "into", "between",
            "האם", "האם", "מה", "של", "על", "בין", "האם",
            "מחייבת", "הופעת",
        }

        return {
            x for x in words
            if x not in stop
        }

    def _relevance(self, query, title, abstract=""):

        q = self._tokens(query)

        if not q:
            return 0.0

        target = self._tokens(
            f"{title or ''} {abstract or ''}"
        )

        if not target:
            return 0.0

        overlap = len(q & target) / len(q)

        # Small bonus for exact phrase fragments.
        qlow = str(query).lower()
        tlow = f"{title or ''} {abstract or ''}".lower()

        phrase_bonus = 0.0

        for token in sorted(q, key=len, reverse=True)[:5]:
            if len(token) >= 6 and token in tlow:
                phrase_bonus += 0.03

        return min(1.0, overlap + phrase_bonus)

    def _filter_results(self, query, results, threshold=0.18):

        accepted = []
        rejected = []

        for item in results:

            title = item.get("title") or ""
            abstract = item.get("abstract") or ""

            score = self._relevance(
                query,
                title,
                abstract
            )

            item["relevance_score"] = round(score, 4)

            if score >= threshold:
                accepted.append(item)
            else:
                rejected.append(item)

        accepted.sort(
            key=lambda x: (
                x.get("relevance_score", 0),
                x.get("citation_count", 0) or
                x.get("cited_by_count", 0) or 0
            ),
            reverse=True
        )

        return accepted, rejected

    # ---------------------------------------------------------
    # OpenAlex
    # ---------------------------------------------------------

    def _openalex(self, question, limit=10):

        query = self._normalize_query(question)

        params = urllib.parse.urlencode({
            "search": query,
            "per-page": limit
        })

        url = (
            "https://api.openalex.org/works?"
            + params
        )

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent":
                    "IMA-Research-Council/5.1 "
                    "(mailto:research@ima.local)"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=20
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

        results = []

        for item in data.get("results", []):

            primary = item.get("primary_location") or {}
            source = primary.get("source") or {}

            authors = []

            for authorship in item.get("authorships") or []:
                author = authorship.get("author") or {}
                name = author.get("display_name")

                if name:
                    authors.append(name)

            results.append({
                "title": item.get("display_name"),
                "abstract": None,
                "year": item.get("publication_year"),
                "doi": item.get("doi"),
                "openalex_id": item.get("id"),
                "type": item.get("type"),
                "authors": authors,
                "journal": source.get("display_name"),
                "cited_by_count": item.get("cited_by_count"),
                "is_open_access": (
                    item.get("open_access") or {}
                ).get("is_oa"),
                "landing_page": primary.get(
                    "landing_page_url"
                ),
                "abstract_available": bool(
                    item.get("abstract_inverted_index")
                )
            })

        return results

    # ---------------------------------------------------------
    # Crossref with retry/backoff
    # ---------------------------------------------------------

    def _crossref(self, question, limit=10):

        query = self._normalize_query(question)

        params = urllib.parse.urlencode({
            "query.bibliographic": query,
            "rows": limit
        })

        url = (
            "https://api.crossref.org/works?"
            + params
        )

        headers = {
            "User-Agent":
                "IMA-Research-Council/5.1 "
                "(mailto:research@ima.local)",
            "Accept": "application/json",
        }

        last_error = None

        for attempt in range(3):

            try:

                request = urllib.request.Request(
                    url,
                    headers=headers
                )

                with urllib.request.urlopen(
                    request,
                    timeout=20
                ) as response:

                    data = json.loads(
                        response.read().decode("utf-8")
                    )

                results = []

                for item in (
                    data.get("message", {})
                    .get("items", [])
                ):

                    authors = []

                    for author in item.get("author") or []:

                        name = " ".join(
                            x for x in [
                                author.get("given"),
                                author.get("family")
                            ]
                            if x
                        )

                        if name:
                            authors.append(name)

                    published = (
                        item.get("published-print")
                        or item.get("published-online")
                        or {}
                    )

                    date_parts = (
                        published.get("date-parts")
                        or [[]]
                    )

                    year = (
                        date_parts[0][0]
                        if date_parts and date_parts[0]
                        else None
                    )

                    results.append({
                        "title": (
                            item.get("title")
                            or [None]
                        )[0],
                        "year": year,
                        "doi": item.get("DOI"),
                        "authors": authors,
                        "journal": (
                            item.get("container-title")
                            or [None]
                        )[0],
                        "type": item.get("type"),
                        "url": item.get("URL")
                    })

                return results

            except HTTPError as e:

                last_error = e

                if e.code == 429:

                    time.sleep(2 ** attempt)
                    continue

                raise

            except Exception as e:

                last_error = e
                time.sleep(1)

        raise last_error

    # ---------------------------------------------------------
    # Main investigation
    # ---------------------------------------------------------

    def investigate(self, question):

        query = self._normalize_query(question)

        errors = []

        # Provider 1: OpenAlex
        try:

            raw = self._openalex(query)

            accepted, rejected = self._filter_results(
                query,
                raw
            )

            if accepted:

                return {
                    "agent": self.name,
                    "status": "ANSWER_READY",
                    "provider": "OpenAlex",
                    "question": question,
                    "normalized_query": query,
                    "result_count": len(accepted),
                    "rejected_count": len(rejected),
                    "sources": accepted,
                    "evidence_type": [
                        "scientific literature",
                        "bibliographic metadata"
                    ],
                    "limitations": [
                        "Bibliographic retrieval is not proof of validity.",
                        "Relevance filtering is heuristic.",
                        "Scientific quality requires paper-level evaluation."
                    ]
                }

        except Exception as e:

            errors.append({
                "provider": "OpenAlex",
                "error": repr(e)
            })

        # Provider 2: Crossref
        try:

            time.sleep(0.25)

            raw = self._crossref(query)

            accepted, rejected = self._filter_results(
                query,
                raw
            )

            return {
                "agent": self.name,
                "status": (
                    "ANSWER_READY"
                    if accepted
                    else "NO_RELEVANT_RESULTS"
                ),
                "provider": "Crossref",
                "question": question,
                "normalized_query": query,
                "result_count": len(accepted),
                "rejected_count": len(rejected),
                "sources": accepted,
                "evidence_type": [
                    "scientific literature",
                    "bibliographic metadata"
                ],
                "limitations": [
                    "Crossref metadata does not establish scientific validity.",
                    "Relevance scoring is heuristic.",
                    "Relevance and evidence quality require further evaluation."
                ],
                "errors": errors
            }

        except Exception as e:

            errors.append({
                "provider": "Crossref",
                "error": repr(e)
            })

        return {
            "agent": self.name,
            "status": "PROVIDER_ERROR",
            "question": question,
            "normalized_query": query,
            "sources": [],
            "errors": errors,
            "contract": (
                "Return scientific papers, evidence, "
                "contradictions and source metadata."
            )
        }
