import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET


def search(question):

    try:
        q=urllib.parse.quote(question)

        url=(
            "https://export.arxiv.org/api/query?"
            "search_query=all:"
            + q +
            "&max_results=1"
        )

        with urllib.request.urlopen(
            url,
            timeout=10
        ) as r:

            xml=r.read()

        root=ET.fromstring(xml)

        ns={
            "a":"http://www.w3.org/2005/Atom"
        }

        entry=root.find(
            "a:entry",
            ns
        )

        if entry is not None:

            title=entry.find(
                "a:title",
                ns
            )

            summary=entry.find(
                "a:summary",
                ns
            )

            link=entry.find(
                "a:id",
                ns
            )

            if summary is not None:

                return {
                    "content":
                        (title.text if title is not None else "")
                        + "\n\n"
                        + summary.text,

                    "source":"arXiv",
                    "url":
                        link.text if link is not None else "",
                    "confidence":0.85
                }

    except Exception:
        pass

    return None
