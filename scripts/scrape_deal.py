import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse

DATA_DIR = Path("data")
INDEX_FILE = DATA_DIR / "deals_index.csv"
RAW_FILE = DATA_DIR / "deals_raw.csv"

index_df = pd.read_csv(INDEX_FILE)

existing = set()
if RAW_FILE.exists():
    existing = set(pd.read_csv(RAW_FILE)["deal_id"].astype(str))

rows = []

for _, row in index_df.iterrows():
    if row.deal_id in existing:
        continue

    html = requests.get(row.deal_url, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")

    buy = soup.select_one("a[href^='http']")
    buy_url = buy["href"] if buy else ""

    platform = ""
    if buy_url:
        platform = urlparse(buy_url).netloc.replace("www.", "").split(".")[0]

    price = soup.find(text=lambda x: x and "₹" in x)

    rows.append({
        "deal_id": row.deal_id,
        "title": row.title,
        "platform": platform,
        "buy_url": buy_url,
        "raw_price_text": price.strip() if price else ""
    })

if rows:
    df_new = pd.DataFrame(rows)
    if RAW_FILE.exists():
        df_old = pd.read_csv(RAW_FILE)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(RAW_FILE, index=False)

