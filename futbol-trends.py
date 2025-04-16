rom pytrends.request import TrendReq
import pandas as pd
import json
from datetime import datetime
import time
import random
import requests
from bs4 import BeautifulSoup

pytrends = TrendReq(hl='en-US', tz=0)

# Your curated keyword map...
# [Shortened for brevity — keep same as before]
keyword_categories = {
    "Lionel Messi": "Global Stars", "Cristiano Ronaldo": "Global Stars", "Kylian Mbappé": "Global Stars",
    "UEFA Champions League": "Tournaments", "FIFA World Cup": "Tournaments",
    "Al Ahly SC": "Africa", "Al Hilal": "Asia", "Real Madrid": "Europe", "MLS": "Americas"
    # Add rest here from your previous script
}

keywords = list(keyword_categories.keys())
categorized_trends = {}

def chunked(iterable, size=5):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

# Curated Trends
for batch in chunked(keywords, 5):
    try:
        pytrends.build_payload(batch, timeframe='now 1-d', geo='')
        related = pytrends.related_queries()
        for kw in batch:
            cat = keyword_categories.get(kw, "Uncategorized")
            if cat not in categorized_trends:
                categorized_trends[cat] = []
            if kw in related and related[kw]['rising'] is not None:
                for _, row in related[kw]['rising'].iterrows():
                    categorized_trends[cat].append({
                        "topic": row['query'],
                        "value": row['value'],
                        "source": kw
                    })
        time.sleep(random.uniform(1, 3))
    except Exception as e:
        print(f"Error in batch {batch}: {e}")

for cat in categorized_trends:
    categorized_trends[cat] = sorted(categorized_trends[cat], key=lambda x: x['value'], reverse=True)[:10]

# General Trends
general_keywords = ["Soccer", "Football", "Fútbol"]
general_trends = []

for keyword in general_keywords:
    try:
        pytrends.build_payload([keyword], timeframe='now 1-d', geo='')
        related = pytrends.related_queries()
        if keyword in related and related[keyword]['rising'] is not None:
            for _, row in related[keyword]['rising'].iterrows():
                general_trends.append({
                    "topic": row['query'],
                    "value": row['value'],
                    "source": keyword
                })
        time.sleep(random.uniform(1, 3))
    except Exception as e:
        print(f"Error in general keyword {keyword}: {e}")

# Forebet Trends with fail-safe
forebet_trends = []
try:
    url = "https://www.forebet.com/en/trends/top"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    trend_boxes = soup.select('.trendsBody .trendRow')

    for box in trend_boxes[:10]:
        team = box.select_one(".trendTeamName").get_text(strip=True) if box.select_one(".trendTeamName") else "Unknown Team"
        trend_text = box.select_one(".trendsStatText").get_text(strip=True) if box.select_one(".trendsStatText") else "No trend text"
        league = box.select_one(".trendTeamLeague").get_text(strip=True) if box.select_one(".trendTeamLeague") else "Unknown League"

        forebet_trends.append({
            "team": team,
            "league": league,
            "trend": trend_text
        })

except Exception as e:
    print("⚠️ Forebet scraping failed:", str(e))
    forebet_trends = []

# Output
output = {
    "last_updated": datetime.utcnow().isoformat() + "Z",
    "categorized_trends": categorized_trends,
    "general_trends": sorted(general_trends, key=lambda x: x['value'], reverse=True)[:10],
    "forebet_trends": forebet_trends,
    "interest_over_time": {}
}

with open("trends.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print("✅ trends.json updated (safe version).")
