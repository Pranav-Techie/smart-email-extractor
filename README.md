# Smart Email Extractor

**Author:** Pranav Kumar Jha  
**GitHub Repository:** [Smart Email Extractor](https://github.com/Pranav-Techie/smart-email-extractor)

---

## Overview

Smart Email Extractor is a Python-based web application that scrapes websites to find valid email addresses intelligently.  
It includes:
- A Flask-based web interface.
- A REST API endpoint for programmatic access.
- Email validation and scoring.
- CSV export of extracted leads.

This tool helps marketers, researchers, and developers automate lead extraction from websites securely and efficiently.

---

## Features

 Extracts emails from any given domain.  
 Validates email format and checks for MX records.  
 Assigns quality scores based on reliability.  
 Exports results to CSV automatically.  
 REST API for external integrations.  
 Includes a Jupyter Notebook API demonstration.

---

## Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, Jinja2  
- **Libraries:** BeautifulSoup4, Requests, dnspython, tldextract, flask-cors  
- **API Testing:** Jupyter Notebook / Postman

---

##  Setup Instructions

### 1 Clone the Repository
```bash
git clone https://github.com/Pranav-Techie/smart-email-extractor.git
cd smart-email-extractor
