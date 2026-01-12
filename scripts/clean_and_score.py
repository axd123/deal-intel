import os
import pandas as pd

RAW_FILE = "data/deals_raw.csv"
SCORED_FILE = "data/deals_scored.csv"

if not os.path.exists(RAW_FILE):
    print(f"{RAW_FILE} not found. Nothing to clean or score.")
    exit(0)

df = pd.read_csv(RAW_FILE)

# Placeholder cleaning & scoring logic
df["title_clean"] = df["title"].str.strip()
df["score"] = 1  # Dummy scoring for now

df.to_csv(SCORED_FILE, index=False)
print(f"Saved cleaned and scored deals to {SCORED_FILE}")
