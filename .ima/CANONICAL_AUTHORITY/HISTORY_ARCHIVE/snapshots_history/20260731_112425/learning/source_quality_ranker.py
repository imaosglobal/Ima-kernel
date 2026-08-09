
WEIGHTS={
"Nature":1.0,
"PubMed":1.0,
"NASA":0.95,
"NOAA":0.95,
"MIT":0.95,
"arXiv":0.9,
"Google Scholar":0.85,
"Wikipedia":0.7,
"DuckDuckGo":0.5
}

def rank(source,trust=0):

    base=WEIGHTS.get(
        source,
        0.4
    )

    return round(
        base*(trust/100 if trust else 1),
        3
    )
