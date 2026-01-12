Deal Intel - DesiDime Scraper v1.2

This repository contains an automated pipeline to scrape, clean, and score online deals from DesiDime (https://www.desidime.com).
Version v1.2 introduces a Playwright-based scraper for JS-rendered content, ensuring all deals are captured accurately.

Features in v1.2:
- Scrapes deals from DesiDime's /new page, including JS-rendered content
- Tracks already-seen deals to avoid duplicates
- Automatically bootstraps deals_index.csv on first run
- Saves raw scraped deals in data/deals_raw.csv
- Cleans and scores deals in data/deals_scored.csv
- Stores index of known deals in data/deals_index.csv
- Supports Amazon and Flipkart platform identification
- Fully automated daily workflow via GitHub Actions

Repository Structure:
deal-intel/
├─ scripts/
│  ├─ scrape_index.py
│  ├─ scrape_deal.py       # Playwright scraper
│  └─ clean_and_score.py
├─ data/
│  ├─ deals_index.csv      # Bootstrapped on first run
│  ├─ deals_raw.csv
│  └─ deals_scored.csv
├─ .github/workflows/
│  └─ daily_desidime_scrape.yml
├─ requirements.txt
└─ README.md

Setup & Requirements:
- Python 3.11+
- Dependencies in requirements.txt:
  pandas>=2.0.0
  beautifulsoup4>=4.12.2
  playwright>=1.41.1
- GitHub Actions workflow installs browsers automatically via:
  playwright install

Usage:

First run (fresh branch / v1.2):
1. Delete any old CSV files in data/:
   data/deals_index.csv
   data/deals_raw.csv
   data/deals_scored.csv
2. Push the branch (e.g., v1.2) to GitHub.
3. Trigger workflow manually or wait for scheduled run.
4. Check data/ for newly created CSVs:
   - deals_index.csv – bootstrapped index
   - deals_raw.csv – raw scraped deals
   - deals_scored.csv – cleaned and scored deals

Subsequent runs:
- Workflow automatically appends new deals only.
- Already-seen deals are skipped.

Workflow:
- GitHub Actions workflow .github/workflows/daily_desidime_scrape.yml
- Triggered by:
  - Push to main or v1.2 branches
  - Scheduled cron (daily at 6:00 UTC)
- Steps:
  1. Checkout repo
  2. Set up Python 3.11
  3. Install dependencies + Playwright browsers
  4. Run scrape_index.py
  5. Run scrape_deal.py
  6. Run clean_and_score.py
  7. Commit updated CSVs to repo

v1.2 Notes / Improvements:
- Playwright handles JS-rendered pages; v1.1 used requests only.
- First-run bootstrap of deals_index.csv ensures smooth fresh start.
- Platform detection (Amazon / Flipkart) improved.
- Fully compatible with GitHub Actions automated daily updates.

Next Steps / Future Versions:
- Track historical prices per deal
- Implement deal scoring based on discount %, category, and median prices
- Extend platform detection to additional e-commerce portals
- Optional web dashboard or Telegram notifications for “good deals”
- 
