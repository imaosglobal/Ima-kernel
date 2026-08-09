
def build_citation(record):

    if not record:
        return ""

    source=record.get("source",{})

    return (
        "\n\nמקור:\n"
        +
        str(source.get("name","לא ידוע"))
        +
        "\n"
        +
        str(source.get("url",""))
        +
        "\nאמינות: "
        +
        str(
            record.get(
                "validation",
                {}
            ).get(
                "confidence",
                0
            )
        )
    )


def should_show_source(message):

    words=[
        "מקור",
        "ציטוט",
        "מאיפה",
        "קישור",
        "reference",
        "source"
    ]

    return any(
        x in message.lower()
        for x in words
    )
