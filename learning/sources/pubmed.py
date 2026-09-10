from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def _terms(question):
    return {
        word.casefold()
        for word in re.findall(r"[A-Za-z0-9]{3,}", question)
    }


def _score(question, title, abstract):
    terms = _terms(question)
    text = f"{title} {abstract}".casefold()

    if not terms:
        return 0

    title_text = title.casefold()
    score = 0

    for term in terms:
        if term in title_text:
            score += 3
        elif term in text:
            score += 1

    return score


def search(question):
    question = str(question).strip()
    if not question:
        return None

    try:
        params = urllib.parse.urlencode({
            "db": "pubmed",
            "term": question,
            "retmode": "json",
            "retmax": "5",
        })

        with urllib.request.urlopen(
            f"{ESEARCH}?{params}",
            timeout=10,
        ) as response:
            data = json.loads(
                response.read().decode("utf-8", errors="ignore")
            )

        ids = data.get("esearchresult", {}).get("idlist", [])
        if not ids:
            return None

        fetch_params = urllib.parse.urlencode({
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "xml",
        })

        with urllib.request.urlopen(
            f"{EFETCH}?{fetch_params}",
            timeout=10,
        ) as response:
            xml = response.read()

        root = ET.fromstring(xml)

        candidates = []

        for article in root.findall(".//PubmedArticle"):
            pmid = article.findtext(".//PMID", default="").strip()
            title = article.findtext(".//ArticleTitle", default="").strip()

            abstract_parts = [
                "".join(node.itertext()).strip()
                for node in article.findall(".//AbstractText")
            ]

            abstract = "\n".join(
                part for part in abstract_parts if part
            )

            if not title and not abstract:
                continue

            score = _score(question, title, abstract)

            candidates.append({
                "pmid": pmid,
                "title": title,
                "abstract": abstract,
                "score": score,
            })

        if not candidates:
            return None

        best = max(candidates, key=lambda item: item["score"])

        if best["score"] <= 0:
            return None

        url = f"https://pubmed.ncbi.nlm.nih.gov/{best['pmid']}/"

        return {
            "content": (
                f"{best['title']}\n\n{best['abstract']}"
            ).strip()[:5000],
            "source": "PubMed",
            "url": url,
            "confidence": min(0.95, 0.70 + best["score"] * 0.03),
            "relevance_score": best["score"],
        }

    except Exception:
        return None
