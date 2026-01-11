import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path

BASE_URL = "https://www.desidime.com/new"
DATA_DIR = Path("data")
INDEX_FILE = DATA_DIR / "deals_index.csv"

DATA_DIR.mkdir(exist_ok=True)

existing = set()
if INDEX_FILE.exists():
    existing = set(pd.read_csv(INDEX_FILE)["deal_id"].astype(str))

rows = []
page = 1
stop = False

while not stop:
    url = f"{BASE_URL}?page={page}"
    html = requests.get(url, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")

    cards = soup.select("div.deal-card")
    if not cards:
        break

    for pos, card in enumerate(cards, start=1):
        link = card.select_one("a[href*='/deals/']")
        if not link:
            continue

        deal_url = "https://www.desidime.com" + link["href"]
        deal_id = deal_url.rstrip("/").split("/")[-1]

        if deal_id in existing:
            stop = True
            break

        title = card.select_one(".deal-title")

        rows.append({
            "deal_id": deal_id,
            "deal_url": deal_url,
            "title": title.get_text(strip=True) if title else "",
            "source_page": page,
            "source_position": pos,
            "seen_count": 1
        })

    page += 1

if rows:
    df_new = pd.DataFrame(rows)

    if INDEX_FILE.exists():
        df_old = pd.read_csv(INDEX_FILE)
        df_old["seen_count"] += df_old["deal_id"].isin(df_new["deal_id"]).astype(int)
        df = pd.concat([df_new, df_old], ignore_index=True)
    else:
        df = df_new

    df.drop_duplicates("deal_id", keep="first", inplace=True)
    df.to_csv(INDEX_FILE, index=False)

