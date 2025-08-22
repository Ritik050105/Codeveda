from flask import Flask, render_template, request, send_file
from scraper import scrape_data
import csv
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = []
    url = ''
    if request.method == 'POST':
        url = request.form['url']
        data = scrape_data(url)
        # Save to CSV
        with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['S.No', 'Headline'])
            for i, item in enumerate(data):
                writer.writerow([i + 1, item])
    return render_template('index.html', data=data, url=url)

@app.route('/download')
def download():
    path = "scraped_data.csv"
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "No data to download!"

if __name__ == '__main__':
    app.run(debug=True)
