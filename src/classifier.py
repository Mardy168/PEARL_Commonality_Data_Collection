def classify_topic(text, topics):
    text = str(text).lower()
    found = []
    for topic, keywords in topics.items():
        if any(k.lower() in text for k in keywords):
            found.append(topic)
    return "; ".join(found) if found else "general"


def source_group(title, url, country=""):
    text = f"{title} {url} {country}".lower()
    cambodia_markers = [
        "cambodia", ".kh", "khmertimeskh", "phnompenhpost", "akp.gov.kh",
        "cambodianess", "camboja", "kampong thom", "siem reap", "preah vihear", "oddar meanchey"
    ]
    return "Cambodia News" if any(m in text for m in cambodia_markers) else "Global Trend"


def relevance_score(row):
    text = f"{row.get('title','')} {row.get('summary','')} {row.get('search_query','')}".lower()
    keywords = [
        "cambodia", "mango", "cashew", "rice", "vegetable", "price", "market",
        "export", "farmer", "climate", "drought", "flood", "policy", "investment",
        "processing", "production", "supply chain", "greenhouse", "ghg", "sustainability"
    ]
    return sum(1 for k in keywords if k in text)
