from __future__ import annotations

import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


API = "https://export.arxiv.org/api/query"


def _terms(question):
    return {
        word.casefold()
        for word in re.findall(r"[A-Za-z0-9]{3,}", str(question))
    }


def _score(question, title, summary):
    terms = _terms(question)
    title_text = title.casefold()
    body = f"{title} {summary}".casefold()

    score = 0
    for term in terms:
        if term in title_text:
            score += 3
        elif term in body:
            score += 1

    return score


def search(question):
    question = str(question).strip()
    if not question:
        return None

    try:
        params = urllib.parse.urlencode({
            "search_query": f"all:{question}",
            "start": "0",
            "max_results": "5",
        })

        with urllib.request.urlopen(
            f"{API}?{params}",
            timeout=10,
        ) as response:
            xml = response.read()

        root = ET.fromstring(xml)
        ns = {"a": "http://www.w3.org/2005/Atom"}

        candidates = []

        for entry in root.findall("a:entry", ns):
            title_node = entry.find("a:title", ns)
            summary_node = entry.find("a:summary", ns)
            link_node = entry.find("a:id", ns)

            title = (
                "".join(title_node.itertext()).strip()
                if title_node is not None
                else ""
            )

            summary = (
                "".join(summary_node.itertext()).strip()
                if summary_node is not None
                else ""
            )

            url = (
                link_node.text.strip()
                if link_node is not None and link_node.text
                else ""
            )

            if not title and not summary:
                continue

            score = _score(question, title, summary)

            candidates.append({
                "title": title,
                "summary": summary,
                "url": url,
                "score": score,
            })

        if not candidates:
            return None

        best = max(candidates, key=lambda item: item["score"])

        if best["score"] <= 0:
            return None

        return {
            "content": f"{best['title']}\n\n{best['summary']}".strip()[:5000],
            "title": best["title"],
            "source": "arXiv",
            "url": best["url"],
            "confidence": min(0.95, 0.75 + best["score"] * 0.03),
            "relevance_score": best["score"],
        }

    except Exception:
        return None
