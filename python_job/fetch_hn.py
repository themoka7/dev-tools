import feedparser
import json
import os

FEED_URL = "https://hnrss.org/frontpage"
OUTPUT = "python_job/data/hn.json"

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

feed = feedparser.parse(FEED_URL)

items = []
for e in feed.entries[:10]:
    items.append({
        "title": e.title,
        "link": e.link,
        "date": e.published
    })

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print("HN feed updated:", len(items))
