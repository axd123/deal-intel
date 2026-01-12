import os
import pandas as pd
from datetime import datetime
from playwright.sync_api import sync_playwright

INDEX_FILE = "data/deals_index.csv"
RAW_FILE = "data/deals_raw.csv"
BASE_URL = "https://www.desidime.com/new"

# Bootstrap index if missing
if not os.path.exists(INDEX_FILE):
    print(f"{INDEX_FILE} not found. Bootstrapping first run.")
    pd.DataFrame(columns=["deal_id", "source", "first_seen_date"]).to_csv(INDEX_FILE, index=False)

index_df = pd.read_csv(INDEX_FILE)
seen_deal_ids = set(index_df["deal_id"].tolist()) if "deal_id" in index_df.columns else set()
print(f"Loaded index with {len(seen_deal_ids)} known deals.")

# Start Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(BASE_URL, timeout=60000)
    
    # Wait for deals container to load
    page.wait_for_selector("a.deal-card", timeout=10000)

    deal_elements = page.query_selector_all("a.deal-card")
    
    if not deal_elements:
        print("No deal cards found on the page.")
        browser.close()
        exit(0)
    
    deals = []
    for elem in deal_elements:
        deal_url = elem.get_attribute("href")
        if not deal_url:
            continue
        deal_id = deal_url.strip("/").split("/")[-1]
        
        if deal_id in seen_deal_ids:
            print(f"Encountered already-seen deal ID {deal_id}, stopping crawl.")
            break
        
        title_tag = elem.query_selector("h3")
        title_text = title_tag.inner_text().strip() if title_tag else "Unknown title"
        
        platform = "Unknown"
        if "amazon" in deal_url.lower():
            platform = "Amazon"
        elif "flipkart" in deal_url.lower():
            platform = "Flipkart"
        
        deals.append({
            "deal_id": deal_id,
            "title": title_text,
            "platform": platform,
            "deal_url": deal_url,
            "scrape_date": datetime.now().strftime("%Y-%m-%d")
        })
    
    browser.close()

# Save raw data
if deals:
    df = pd.DataFrame(deals)
    df.to_csv(RAW_FILE, index=False)
    print(f"Saved {len(df)} new deals to {RAW_FILE}")
else:
    print("No new deals scraped. Nothing to save.")
