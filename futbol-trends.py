from pytrends.request import TrendReq
import pandas as pd
import json
from datetime import datetime
import time
import random

pytrends = TrendReq(hl='en-US', tz=0)

keyword_categories = {
    "Lionel Messi": "Global Stars", "Cristiano Ronaldo": "Global Stars", "Kylian Mbappé": "Global Stars",
    "Erling Haaland": "Global Stars", "Mohamed Salah": "Global Stars", "Vinícius Jr": "Global Stars",
    "Neymar": "Global Stars", "Jude Bellingham": "Global Stars", "Heung-Min Son": "Global Stars",
    "UEFA Champions League": "Tournaments", "Europa League": "Tournaments", "Conference League": "Tournaments",
    "FIFA World Cup": "Tournaments", "Women's World Cup": "Tournaments", "Club World Cup": "Tournaments",
    "Copa América": "Tournaments", "AFCON": "Tournaments", "Asian Cup": "Tournaments", "Gold Cup": "Tournaments",
    "CAF Champions League": "Tournaments", "Copa Libertadores": "Tournaments", "Copa Sudamericana": "Tournaments",
    "AFC Champions League": "Tournaments", "Al Ahly SC": "Africa", "Zamalek SC": "Africa",
    "Wydad Casablanca": "Africa", "Esperance de Tunis": "Africa", "Mamelodi Sundowns": "Africa",
    "TP Mazembe": "Africa", "Egypt Cup": "Africa", "MTN8": "Africa", "Al Hilal": "Asia", "Al Nassr": "Asia",
    "Urawa Red Diamonds": "Asia", "Kawasaki Frontale": "Asia", "Melbourne Victory": "Asia", "J1 League": "Asia",
    "K League": "Asia", "Indian Super League": "Asia", "Saudi Pro League": "Asia", "King's Cup": "Asia",
    "Real Madrid": "Europe", "FC Barcelona": "Europe", "Manchester United": "Europe", "Manchester City": "Europe",
    "Liverpool FC": "Europe", "Arsenal": "Europe", "Bayern Munich": "Europe", "Juventus": "Europe",
    "Inter Milan": "Europe", "Paris Saint-Germain": "Europe", "Premier League": "Europe", "La Liga": "Europe",
    "Serie A": "Europe", "Bundesliga": "Europe", "Ligue 1": "Europe", "Eredivisie": "Europe",
    "Copa del Rey": "Europe", "DFB Pokal": "Europe", "FA Cup": "Europe", "MLS": "Americas", "Liga MX": "Americas",
    "Boca Juniors": "Americas", "River Plate": "Americas", "Flamengo": "Americas", "Corinthians": "Americas",
    "Palmeiras": "Americas", "Club América": "Americas", "Seattle Sounders": "Americas",
    "Atlanta United": "Americas", "US Open Cup": "Americas", "Campeonato Brasileiro Série A": "Americas"
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

# Simulated WhoScored Trends
whoscored_trends = [
    {"team": "Manchester City", "league": "Premier League", "trend": "5-game winning streak, dominant form"},
    {"team": "Bayern Munich", "league": "Bundesliga", "trend": "Unbeaten in last 7 matches, strong away record"},
    {"team": "Paris Saint-Germain", "league": "Ligue 1", "trend": "Leading the league with highest goal difference"},
    {"player": "Lionel Messi", "league": "MLS", "trend": "Avg rating 8.5 in last 5 matches"},
    {"player": "Erling Haaland", "league": "Premier League", "trend": "Scoring in 6 consecutive appearances"},
    {"match": "Real Madrid vs Barcelona", "competition": "La Liga", "trend": "Both teams in top form ahead of El Clásico"},
    {"match": "Inter Milan vs AC Milan", "competition": "Serie A", "trend": "Derby approaching with title race impact"}
]

# Final JSON
output = {
    "last_updated": datetime.utcnow().isoformat() + "Z",
    "categorized_trends": categorized_trends,
    "general_trends": sorted(general_trends, key=lambda x: x['value'], reverse=True)[:10],
    "whoscored_trends": whoscored_trends,
    "interest_over_time": {}
}

with open("trends.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print("✅ trends.json updated with curated, general, and WhoScored trends.")
