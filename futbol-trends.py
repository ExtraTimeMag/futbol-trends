from pytrends.request import TrendReq
import pandas as pd
import json
from datetime import datetime

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=0)

# Keywords grouped by category
keyword_categories = {
    # 🌍 Global Stars
    "Lionel Messi": "Global Stars",
    "Cristiano Ronaldo": "Global Stars",
    "Kylian Mbappé": "Global Stars",
    "Erling Haaland": "Global Stars",
    "Mohamed Salah": "Global Stars",
    "Vinícius Jr": "Global Stars",
    "Neymar": "Global Stars",
    "Jude Bellingham": "Global Stars",
    "Heung-Min Son": "Global Stars",

    # 🏆 Major Tournaments
    "UEFA Champions League": "Tournaments",
    "Europa League": "Tournaments",
    "Conference League": "Tournaments",
    "EURO 2024": "Tournaments",
    "FIFA World Cup": "Tournaments",
    "Women's World Cup": "Tournaments",
    "Club World Cup": "Tournaments",
    "Copa América": "Tournaments",
    "AFCON": "Tournaments",
    "Asian Cup": "Tournaments",
    "Gold Cup": "Tournaments",
    "Copa Libertadores": "Tournaments",
    "Copa Sudamericana": "Tournaments",

    # 🇪🇺 European Clubs & Leagues
    "Real Madrid": "Europe",
    "FC Barcelona": "Europe",
    "Manchester United": "Europe",
    "Manchester City": "Europe",
    "Liverpool FC": "Europe",
    "Arsenal": "Europe",
    "Bayern Munich": "Europe",
    "Juventus": "Europe",
    "Inter Milan": "Europe",
    "Paris Saint-Germain": "Europe",
    "Premier League": "Europe",
    "La Liga": "Europe",
    "Serie A": "Europe",
    "Bundesliga": "Europe",
    "Ligue 1": "Europe",
    "Eredivisie": "Europe",

    # 🌎 Americas
    "MLS": "Americas",
    "Liga MX": "Americas",
    "Boca Juniors": "Americas",
    "River Plate": "Americas",
    "Flamengo": "Americas",
    "Corinthians": "Americas",
    "Palmeiras": "Americas",
    "Club América": "Americas",
    "Seattle Sounders": "Americas",
    "Atlanta United": "Americas",

    # 🌍 Africa
    "Al Ahly SC": "Africa",
    "Zamalek SC": "Africa",
    "Wydad Casablanca": "Africa",
    "Esperance de Tunis": "Africa",
    "Mamelodi Sundowns": "Africa",
    "TP Mazembe": "Africa",
    "CAF Champions League": "Africa",

    # 🌏 Asia & Oceania
    "Al Hilal": "Asia",
    "Al Nassr": "Asia",
    "Urawa Red Diamonds": "Asia",
    "Kawasaki Frontale": "Asia",
    "Melbourne Victory": "Asia",
    "J1 League": "Asia",
    "K League": "Asia",
    "Indian Super League": "Asia",

    # 🏟 Other Leagues & Cups
    "Turkish Süper Lig": "Other Leagues",
    "Saudi Pro League": "Other Leagues",
    "Egypt Cup": "Other Leagues",
    "FA Cup": "Other Leagues",
    "Copa del Rey": "Other Leagues",
    "DFB Pokal": "Other Leagues",
    "US Open Cup": "Other Leagues",
    "Campeonato Brasileiro Série A": "Other Leagues",
    "MTN8": "Other Leagues",
    "King's Cup": "Other Leagues",
    "AFC Champions League": "Other Leagues"
}

keywords = list(keyword_categories.keys())

# Get related rising queries
pytrends.build_payload(keywords, timeframe='now 1-d', geo='')
related_queries = pytrends.related_queries()

# Group by category
categorized_trends = {}
for kw in keywords:
    category = keyword_categories[kw]
    if category not in categorized_trends:
        categorized_trends[category] = []

    if kw in related_queries:
        rising = related_queries[kw]['rising']
        if rising is not None:
            for _, row in rising.iterrows():
                categorized_trends[category].append({
                    "topic": row['query'],
                    "value": row['value'],
                    "source": kw
                })

# Sort and trim to top 5 per category
for category in categorized_trends:
    categorized_trends[category] = sorted(categorized_trends[category], key=lambda x: x['value'], reverse=True)[:5]

# Get interest over time for top global terms
highlight_terms = ["Lionel Messi", "Cristiano Ronaldo", "UEFA Champions League", "Copa América"]
pytrends.build_payload(highlight_terms, timeframe='now 7-d', geo='')
interest_df = pytrends.interest_over_time().drop(columns='isPartial')

interest_over_time = {}
for term in highlight_terms:
    interest_over_time[term] = interest_df[term].reset_index().to_dict(orient='records')

# Output JSON
final_output = {
    "last_updated": datetime.utcnow().isoformat() + "Z",
    "categorized_trends": categorized_trends,
    "interest_over_time": interest_over_time
}

# Save JSON
with open("trends.json", "w", encoding="utf-8") as f:
    json.dump(final_output, f, indent=2)

print("✅ trends.json created successfully.")