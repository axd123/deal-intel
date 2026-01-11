import pandas as pd
import re
from pathlib import Path

DATA_DIR = Path("data")
RAW_FILE = DATA_DIR / "deals_raw.csv"
CLEAN_FILE = DATA_DIR / "deals_clean.csv"

df = pd.read_csv(RAW_FILE)

def extract_price(text):
    if not isinstance(text, str):
        return None
    nums = re.findall(r"\d[\d,]*", text)
    return int(nums[0].replace(",", "")) if nums else None

df["price"] = df["raw_price_text"].apply(extract_price)

df["discount_rank"] = df["price"].rank(ascending=True, method="dense")

df.to_csv(CLEAN_FILE, index=False)

