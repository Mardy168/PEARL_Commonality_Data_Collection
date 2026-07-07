import json
import os
import time
from datetime import datetime, timezone

import pandas as pd

from src.classifier import classify_topic, relevance_score, source_group
from src.drive_utils import upload_file_to_subfolder
from src.news_sources import gdelt_news, google_news

ROOT_DRIVE_FOLDER_ID = os.environ.get("GOOGLE_DRIVE_FOLDER_ID")
OUTPUT_DIR = "output"
CONFIG_FILE = "config/keywords.json"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    if not ROOT_DRIVE_FOLDER_ID:
        raise RuntimeError("Missing GOOGLE_DRIVE_FOLDER_ID secret/environment variable.")

    config = load_config()
    crops = config["crops"]
    topics = config["topics"]

    today = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_rows = []
    for crop, queries in crops.items():
        for query in queries:
            print(f"Collecting: {crop} | {query}")
            rows = []
            rows.extend(google_news(query, limit=20))
            rows.extend(gdelt_news(query, limit=50))

            for row in rows:
                row["date_collected"] = today
                row["crop"] = crop
                row["search_query"] = query
                row["topic"] = classify_topic(row.get("title", "") + " " + row.get("summary", ""), topics)
                row["source_group"] = source_group(row.get("title", ""), row.get("url", ""), row.get("country", ""))
                row["relevance_score"] = relevance_score({**row, "search_query": query})
                row["pearl_relevance"] = "High" if row["relevance_score"] >= 5 else "Medium" if row["relevance_score"] >= 3 else "Low"
                row["citation"] = f"{row.get('title','')}. {row.get('source','')}. {row.get('url','')}"
                all_rows.append(row)
            time.sleep(1)

    df = pd.DataFrame(all_rows)
    if df.empty:
        print("No articles collected.")
        return

    df = df.drop_duplicates(subset=["url"])
    df = df.sort_values(["crop", "source_group", "relevance_score"], ascending=[True, True, False])

    xlsx_path = os.path.join(OUTPUT_DIR, f"PEARL_commonality_news_{today}.xlsx")
    csv_path = os.path.join(OUTPUT_DIR, f"PEARL_commonality_news_{today}.csv")

    df.to_excel(xlsx_path, index=False)
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    upload_file_to_subfolder(xlsx_path, ROOT_DRIVE_FOLDER_ID, f"01_Daily_News/{today}")
    upload_file_to_subfolder(csv_path, ROOT_DRIVE_FOLDER_ID, f"01_Daily_News/{today}")

    print(f"Daily collection complete. Articles: {len(df)}")


if __name__ == "__main__":
    main()
