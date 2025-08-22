from flask import Flask, render_template, request, send_from_directory
from scraper import scrape_data
import os
import csv
from datetime import datetime

app = Flask(__name__)
SCRAPE_DIR = "scraped"
if not os.path.exists(SCRAPE_DIR):
    os.makedirs(SCRAPE_DIR)

history = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        heading = request.form["heading"]
        data = scrape_data(url)
        if data:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{heading.replace(' ', '_')}_{timestamp}.csv"
            filepath = os.path.join(SCRAPE_DIR, filename)
            with open(filepath, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Data"])
                for d in data:
                    writer.writerow([d])
            history.append({"heading": heading, "filename": filename})
            return render_template("index.html", latest=data, history=history)
        else:
            return render_template("index.html", error="No data scraped.", history=history)
    return render_template("index.html", history=history)

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(SCRAPE_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
