
def rank(source):
    weights={
        "arXiv":9,
        "Nature":9,
        "PubMed":8,
        "NASA":8,
        "DuckDuckGo":5
    }
    return weights.get(source,1)
