from flask import Flask, request, jsonify, render_template, send_file
from quick_lead_scraper import scrape_domain, save_csv
import os

app = Flask(__name__)

# 🏠 Home page — loads templates/index.html
@app.route("/")
def home():
    return render_template("index.html")

# 📨 Scrape route — runs your scraper logic
@app.route("/scrape", methods=["POST"])
def scrape():
    url = request.form.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400
    
    # Run the scraper
    rows = scrape_domain(url)
    save_csv(rows)  # Save results to leads.csv
    
    # Return results as JSON
    return jsonify({"emails": rows})

# 💾 Route to download the CSV file
@app.route("/download")
def download_csv():
    filepath = "leads.csv"
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({"error": "No CSV file found. Run a scrape first!"}), 404


if __name__ == "__main__":
    app.run(debug=True)

