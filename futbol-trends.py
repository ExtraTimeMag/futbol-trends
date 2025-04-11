
from pytrends.request import TrendReq
import pandas as pd
import json
from datetime import datetime
import time

pytrends = TrendReq(hl='en-US', tz=0)

# Keyword to category mapping
keyword_categories = {
    "Lionel Messi": "Global Stars", "Cristiano Ronaldo": "Global Stars", "Kylian Mbappé": "Global Stars",
    "Erling Haaland": "Global Stars", "Mohamed Salah": "Global Stars", "Vinícius Jr": "Global Stars",
    "Neymar": "Global Stars", "Jude Bellingham": "Global Stars", "Heung-Min Son": "Global Stars",

    "UEFA Champions League": "Tournaments", "Europa League": "Tournaments", "Conference League": "Tournaments",
    "EURO 2024": "Tournaments", "FIFA World Cup": "Tournaments", "Women's World Cup": "Tournaments",
    "Club World Cup": "Tournaments", "Copa América": "Tournaments", "AFCON": "Tournaments",
    "Asian Cup": "Tournaments", "Gold Cup": "Tournaments", "CAF Champions League": "Tournaments",
    "Copa Libertadores": "Tournaments", "Copa Sudamericana": "Tournaments", "AFC Champions League": "Tournaments",

    "Al Ahly SC": "Africa", "Zamalek SC": "Africa", "Wydad Casablanca": "Africa", "Esperance de Tunis": "Africa",
    "Mamelodi Sundowns": "Africa", "TP Mazembe": "Africa", "Egypt Cup": "Africa", "MTN8": "Africa",

    "Al Hilal": "Asia", "Al Nassr": "Asia", "Urawa Red Diamonds": "Asia", "Kawasaki Frontale": "Asia",
    "Melbourne Victory": "Asia", "J1 League": "Asia", "K League": "Asia", "Indian Super League": "Asia",
    "Saudi Pro League": "Asia", "King's Cup": "Asia",

    "Real Madrid": "Europe", "FC Barcelona": "Europe", "Manchester United": "Europe", "Manchester City": "Europe",
    "Liverpool FC": "Europe", "Arsenal": "Europe", "Bayern Munich": "Europe", "Juventus": "Europe",
    "Inter Milan": "Europe", "Paris Saint-Germain": "Europe", "Premier League": "Europe", "La Liga": "Europe",
    "Serie A": "Europe", "Bundesliga": "Europe", "Ligue 1": "Europe", "Eredivisie": "Europe", "Copa del Rey": "Europe",
    "DFB Pokal": "Europe", "FA Cup": "Europe",

    "MLS": "Americas", "Liga MX": "Americas", "Boca Juniors": "Americas", "River Plate": "Americas",
    "Flamengo": "Americas", "Corinthians": "Americas", "Palmeiras": "Americas", "Club América": "Americas",
    "Seattle Sounders": "Americas", "Atlanta United": "Americas", "US Open Cup": "Americas",
    "Campeonato Brasileiro Série A": "Americas"
}

keywords = list(keyword_categories.keys())
categorized_trends = {}

def chunked(iterable, size=5):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

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
        time.sleep(1)
    except Exception as e:
        print(f"Error in batch {batch}: {e}")

# Limit to top 5 trends per category
for cat in categorized_trends:
    categorized_trends[cat] = sorted(categorized_trends[cat], key=lambda x: x['value'], reverse=True)[:5]

# Output
output = {
    "last_updated": datetime.utcnow().isoformat() + "Z",
    "categorized_trends": categorized_trends,
    "interest_over_time": {}
}

with open("trends.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print("✅ trends.json updated (real categories, no charts).")
