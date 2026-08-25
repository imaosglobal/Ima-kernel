
import json
import urllib.parse
import urllib.request
import urllib.error


class SemanticScholarAgent:

    name = "SEMANTIC_SCHOLAR"

    def investigate(self, question):

        base = "https://api.semanticscholar.org/graph/v1/paper/search"

        params = urllib.parse.urlencode({
            "query": question,
            "limit": 10,
            "fields": (
                "title,abstract,year,authors,url,"
                "citationCount,venue,publicationTypes"
            ),
        })

        url = base + "?" + params

        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "IMA-Research-Council/5.0"
                },
            )

            with urllib.request.urlopen(req, timeout=20) as response:
                payload = json.loads(
                    response.read().decode("utf-8")
                )

            papers = []

            for item in payload.get("data", []):
                papers.append({
                    "title": item.get("title"),
                    "abstract": item.get("abstract"),
                    "year": item.get("year"),
                    "authors": [
                        a.get("name")
                        for a in item.get("authors", [])
                    ],
                    "url": item.get("url"),
                    "citation_count": item.get(
                        "citationCount"
                    ),
                    "venue": item.get("venue"),
                    "publication_types": item.get(
                        "publicationTypes"
                    ),
                })

            return {
                "agent": self.name,
                "status": "ANSWER_READY",
                "question": question,
                "provider": "Semantic Scholar",
                "papers": papers,
                "count": len(papers),
                "evidence_type": [
                    "scientific literature",
                    "bibliographic metadata",
                ],
                "limitations": [
                    "Search relevance is not proof of truth.",
                    "Citation count is not evidence quality.",
                    "Individual papers require independent evaluation.",
                ],
            }

        except Exception as e:

            return {
                "agent": self.name,
                "status": "ERROR",
                "question": question,
                "provider": "Semantic Scholar",
                "error": repr(e),
            }
