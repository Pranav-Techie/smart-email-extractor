# 📨 Smart Email Extractor & Validator

A simple Python tool that extracts emails from a website, validates them, scores their quality, and saves the results to a CSV file.

---

##  Features
- Extracts all visible emails from a website.
- Validates emails using domain (MX record check).
- Scores email quality based on:
  - Domain match
  - Non-generic address (not info@, admin@, etc.)
  - MX record presence
- Removes duplicates automatically.
- Exports clean results to `leads.csv`.

---

##  Tech Stack
- Python 3
- Libraries: `requests`, `beautifulsoup4`, `tldextract`, `dnspython`

---

## ⚙️ Setup & Run

```bash
git clone https://github.com/Pranav-Techie/smart-email-extractor
cd smart-email-extractor
pip install -r requirements.txt
python quick_lead_scraper.py
