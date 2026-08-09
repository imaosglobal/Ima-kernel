from learning.sources.html_extractor import extract_text
import urllib.request
import urllib.parse
import json


def search(question):

    try:
        q=urllib.parse.quote(question)

        url=(
            "https://api.duckduckgo.com/"
            "?q="+q+
            "&format=json"
        )

        with urllib.request.urlopen(
            url,
            timeout=8
        ) as r:

            data=json.loads(
                r.read().decode("utf8")
            )


        text=data.get("AbstractText","")

        if text:
            return {
                "content":text,
                "source":"DuckDuckGo",
                "url":data.get("AbstractURL",""),
                "confidence":0.75
            }


        topics=data.get("RelatedTopics",[])

        for item in topics:
            if isinstance(item,dict):

                text=item.get("Text","")

                if text:

                    return {
                        "content":text,
                        "source":"DuckDuckGo",
                        "url":item.get("FirstURL",""),
                        "confidence":0.65
                    }


    except Exception:
        pass


    return None
