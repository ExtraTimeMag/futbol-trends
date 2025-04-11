from pytrends.request import TrendReq
import pandas as pd
import json
from datetime import datetime
import time

pytrends = TrendReq(hl='en-US', tz=0)

# Full keyword list
keywords = [
    "Lionel Messi", "Cristiano Ronaldo", "Kylian Mbappé", "Erling Haaland",
    "Mohamed Salah", "Vinícius Jr", "Neymar", "Jude Bellingham", "Heung-Min Son",
    "UEFA Champions League", "Europa League", "Conference League", "EURO 2024",
    "FIFA World Cup", "Women's World Cup", "Club World Cup", "Copa América", "AFCON",
    "Asian Cup", "Gold Cup", "Copa Libertadores", "Copa Sudamericana",
    "Real Madrid", "FC Barcelona", "Manchester United", "Manchester City", "Liverpool FC",
    "Arsenal", "Bayern Munich", "Juventus", "Inter Milan", "Paris Saint-Germain",
    "Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1", "Eredivisie",
    "MLS", "Liga MX", "Boca Juniors", "River Plate", "Flamengo", "Corinthians",
    "Palmeiras", "Club América", "Seattle Sounders", "Atlanta United",
    "Al Ahly SC", "Zamalek SC", "Wydad Casablanca", "Esperance de Tunis", "Mamelodi Sundowns",
    "TP Mazembe", "CAF Champions League", "Al Hilal", "Al Nassr", "Urawa Red Diamonds",
    "Kawasaki Frontale", "Melbourne Victory", "J1 League", "K League", "Indian Super League",
    "Turkish Süper Lig", "Saudi Pro League", "Egypt Cup", "FA Cup", "Copa del Rey", "DFB Pokal",
    "US Open Cup", "Campeonato Brasileiro Série A", "MTN8", "King's Cup", "AFC Champions League"
]

keyword_categories = {kw: "General" for kw in keywords}
categorized_trends = {}

# Batch helper
def chunked(iterable, size=5):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

# Collect rising queries
for batch in chunked(keywords, 5):
    try:
        pytrends.build_payload(batch, timeframe='now 1-d', geo='')
        related = pytrends.related_queries()
        for kw in batch:
            cat = keyword_categories.get(kw, "General")
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

# Top 5 trends per category
for cat in categorized_trends:
    categorized_trends[cat] = sorted(categorized_trends[cat], key=lambda x: x['value'], reverse=True)[:5]

highlight_terms = ["Lionel Messi", "Cristiano Ronaldo", "UEFA Champions League", "Copa América"]
interest_over_time = {}

for term in highlight_terms:
    try:
        pytrends.build_payload([term], timeframe='now 7-d', geo='')
        df = pytrends.interest_over_time()
        if not df.empty and 'isPartial' in df.columns:
            df = df.drop(columns='isPartial')
        interest_over_time[term] = df[term].reset_index().to_dict(orient='records')
        time.sleep(1)
    except Exception as e:
        print(f"Failed to fetch interest over time for {term}: {e}")

# Write JSON
output = {
    "last_updated": datetime.utcnow().isoformat() + "Z",
    "categorized_trends": categorized_trends,
    "interest_over_time": interest_over_time
}

with open("trends.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print("✅ trends.json updated.")
