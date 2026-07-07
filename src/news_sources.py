import requests
import feedparser
from urllib.parse import quote_plus


def google_news(query, limit=20):
    url = "https://news.google.com/rss/search?q=" + quote_plus(query) + "&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    rows = []
    for entry in feed.entries[:limit]:
        rows.append({
            "published_date": entry.get("published", ""),
            "title": entry.get("title", ""),
            "source": "Google News RSS",
            "country": "",
            "language": "en",
            "url": entry.get("link", ""),
            "summary": entry.get("summary", "")
        })
    return rows


def gdelt_news(query, limit=50):
    api = "https://api.gdeltproject.org/api/v2/doc/doc"
    params = {
        "query": query,
        "mode": "ArtList",
        "format": "json",
        "maxrecords": limit,
        "sort": "HybridRel"
    }
    rows = []
    try:
        r = requests.get(api, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        for a in data.get("articles", []):
            rows.append({
                "published_date": a.get("seendate", ""),
                "title": a.get("title", ""),
                "source": a.get("domain", ""),
                "country": a.get("sourcecountry", ""),
                "language": a.get("language", ""),
                "url": a.get("url", ""),
                "summary": ""
            })
    except Exception as e:
        print(f"GDELT error for {query}: {e}")
    return rows
