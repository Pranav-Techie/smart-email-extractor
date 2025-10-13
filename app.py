from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from quick_lead_scraper import scrape_domain, save_csv
import os

app = Flask(__name__)
CORS(app)

CSV_DIR = "saved_leads"
os.makedirs(CSV_DIR, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url', '').strip()
    print("Received URL:", url)
    if not url:
        return render_template('index.html', error="Please enter a URL.")

    try:
        results = scrape_domain(url)
        print("Scrape results:", results)
        filename = None
        if results:
            filename = save_csv(results, out_dir=CSV_DIR)
        else:
            print("No emails found.")
        return render_template('index.html', results=results, url=url, csvfile=filename)
    except Exception as e:
        print("Error while scraping:", e)
        return render_template('index.html', error=str(e))


@app.route('/scrape_api', methods=['GET'])
def scrape_api():
    url = request.args.get('url', '').strip()
    if not url:
        return jsonify({'error': 'Missing url parameter'}), 400

    try:
        results = scrape_domain(url)
        filename = None
        if results:
            filename = save_csv(results, out_dir=CSV_DIR)
        return jsonify({'results': results, 'csvfile': filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download_csv')
def download_csv():
    filename = request.args.get('file', '').strip()
    if not filename:
        return "Missing file parameter", 400

    if "/" in filename or "\\" in filename:
        return "Invalid filename", 400

    file_path = os.path.join(CSV_DIR, filename)
    if not os.path.exists(file_path):
        return "File not found", 404

    return send_from_directory(CSV_DIR, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
