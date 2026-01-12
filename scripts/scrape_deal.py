import os
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

INDEX_FILE = "data/deals_index.csv"
RAW_FILE = "data/deals_raw.csv"

# Load or bootstrap index
if not os.path.exists(INDEX_FILE):
    print(f"{INDEX_FILE} not found. Bootstrapping first run.")
    pd.DataFrame(columns=["deal_id", "source", "first_seen_date"]).to_csv(INDEX_FILE, index=False)

index_df = pd.read_csv(INDEX_FILE)
seen_deal_ids = set(index_df["deal_id"].tolist()) if "deal_id" in index_df.columns else set()

# URL to scrape
BASE_URL = "https://www.desidime.com/new"
print(f"Scraping deals from {BASE_URL}")

response = requests.get(BASE_URL)
if response.status_code != 200:
    print(f"Failed to fetch {BASE_URL}: {response.status_code}")
    sys.exit(1)

soup = BeautifulSoup(response.text, "html.parser")
deal_cards = soup.find_all("a", class_="deal-card-link")

if not deal_cards:
    print("No deal cards found on the page.")
    sys.exit(0)

# Collect deals
deals = []
for card in deal_cards:
    deal_url = card.get("href")
    if not deal_url:
        continue
    deal_id = deal_url.strip("/").split("/")[-1]
    if deal_id in seen_deal_ids:
        print(f"Encountered already-seen deal ID {deal_id}, stopping crawl.")
        break

    title_tag = card.find("h3")
    title = title_tag.text.strip() if title_tag else "Unknown title"
    platform = "Unknown"
    if "amazon" in deal_url.lower():
        platform = "Amazon"
    elif "flipkart" in deal_url.lower():
        platform = "Flipkart"

    deals.append({
        "deal_id": deal_id,
        "title": title,
        "platform": platform,
        "deal_url": deal_url,
        "scrape_date": datetime.now().strftime("%Y-%m-%d")
    })

# Save raw data if any new deals found
if deals:
    df = pd.DataFrame(deals)
    df.to_csv(RAW_FILE, index=False)
    print(f"Saved {len(df)} new deals to {RAW_FILE}")
else:
    print("No new deals scraped. Nothing to save.")
