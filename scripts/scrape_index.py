import os
import pandas as pd
from datetime import datetime

INDEX_FILE = "data/deals_index.csv"

# Bootstrap first run if index does not exist
if not os.path.exists(INDEX_FILE):
    print(f"{INDEX_FILE} not found. Creating new index for first run.")
    pd.DataFrame(columns=["deal_id", "source", "first_seen_date"]).to_csv(INDEX_FILE, index=False)

# Load existing index
index_df = pd.read_csv(INDEX_FILE)
seen_deal_ids = set(index_df["deal_id"].tolist()) if "deal_id" in index_df.columns else set()
print(f"Loaded index with {len(seen_deal_ids)} known deals.")

# Normally, here you might update the index with new deal IDs after scraping
# Placeholder logic; actual updates happen in scrape_deal.py
