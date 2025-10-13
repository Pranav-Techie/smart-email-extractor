import re
import csv
import time
import requests
import tldextract
from bs4 import BeautifulSoup
import dns.resolver

# Expression to match email addresses
EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', re.IGNORECASE)


def find_emails_from_html(html):
    """Extract emails from plain text and mailto links."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ")
    emails = set(EMAIL_RE.findall(text))

    
    for a in soup.find_all("a", href=True):
        if a['href'].startswith("mailto:"):
            email = a['href'].split("mailto:")[1].split("?")[0]
            emails.add(email)

    return emails


def has_mx(domain):
    """Check if the domain has MX (mail exchange) records."""
    try:
        answers = dns.resolver.resolve(domain, 'MX', lifetime=5)
        return len(answers) > 0
    except Exception:
        return False


def validate_and_score(email, target_domain):
    """Validate email and assign a quality score."""
    if "@" not in email:
        return "invalid", 0

    local, domain = email.rsplit("@", 1)
    score = 0
    status = "invalid"

    if re.fullmatch(EMAIL_RE, email):
        status = "syntax-ok"
        score += 1

        # Check if it belongs to same target domain
        if domain.lower() == target_domain.lower():
            score += 2

        # Non-generic local part (bonus)
        if not any(role in local.lower() for role in ["info", "admin", "sales", "support"]):
            score += 1

        # Domain has MX record
        if has_mx(domain):
            score += 2
            status = "mx-ok"

    return status, score


def scrape_domain(seed_url, max_pages=10, delay=1.0):
    """Crawl pages under same domain and collect emails."""
    print(f"🔍 Starting scrape for: {seed_url}")

    try:
        domain = tldextract.extract(seed_url).registered_domain
        if not domain:
            print("Invalid domain.")
            return []
    except Exception as e:
        print(f" Domain extraction failed: {e}")
        return []

    visited, to_visit, results = set(), {seed_url}, []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop()
        if url in visited:
            continue
        visited.add(url)

        try:
            r = requests.get(url, timeout=10, headers={"User-Agent": "SmartEmailBot/1.0"})
            if "text/html" not in r.headers.get("Content-Type", ""):
                continue
        except Exception as e:
            print(f" Skipping {url}: {e}")
            continue

        # Extracting  and validating emails
        emails = find_emails_from_html(r.text)
        for e in emails:
            status, score = validate_and_score(e, domain)
            results.append({"email": e, "source": url, "status": status, "score": score})

    
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.find_all("a", href=True):
            link = a['href']
            if link.startswith("/"):
                link = requests.compat.urljoin(seed_url, link)
            if link.startswith("http") and domain in link and link not in visited:
                to_visit.add(link)

        time.sleep(delay)

   
    clean = {}
    for r in results:
        e = r['email'].lower()
        if e not in clean or r['score'] > clean[e]['score']:
            clean[e] = r

    print(f" Scraped results: {list(clean.values())}")
    return list(clean.values())


def save_csv(rows, filename="leads.csv"):
    """Save the results to a CSV file."""
    if not rows:
        print(" No data to save.")
        return

    keys = ["email", "source", "status", "score"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)

    print(f"💾 Saved {len(rows)} emails to {filename}")


if __name__ == "__main__":
    seed = input("Enter website URL (e.g., https://example.com): ").strip()
    rows = scrape_domain(seed)
    save_csv(rows)
    print(f" Done! Found {len(rows)} emails.")
