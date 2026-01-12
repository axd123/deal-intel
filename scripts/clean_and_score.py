import pandas as pd
import os
import sys

RAW_FILE = "data/deals_raw.csv"
OUTPUT_FILE = "data/deals_scored.csv"

# Gracefully exit if no raw data exists
if not os.path.exists(RAW_FILE):
    print(f"{RAW_FILE} not found. Nothing to clean or score.")
    sys.exit(0)

# Load raw data
df = pd.read_csv(RAW_FILE)

# Basic cleaning
df = df.drop_duplicates(subset=["deal_id"])

# Convert price columns to numeric where possible
for col in ["regular_price", "offer_price", "discount_percent"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Simple scoring logic (v1.1)
# Higher discount = better score
if "discount_percent" in df.columns:
    df["deal_score"] = df["discount_percent"].fillna(0)
else:
    df["deal_score"] = 0

# Save scored deals
df.to_csv(OUTPUT_FILE, index=False)

print(f"Scored deals written to {OUTPUT_FILE}")
