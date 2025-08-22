from flask import Flask, render_template, request, jsonify
import requests
import requests_cache
import datetime

app = Flask(__name__)
requests_cache.install_cache('crypto_cache', expire_after=60)

@app.route('/')
def index():
    return render_template('index.html', price=None)

@app.route('/price', methods=['POST'])
def price():
    crypto = request.form['crypto']
    currency = request.form['currency']
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": crypto.lower(), "vs_currencies": currency.lower()}

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        price = res.json().get(crypto.lower(), {}).get(currency.lower(), None)
        if price:
            return render_template('index.html', price=price, crypto=crypto, currency=currency)
    except:
        pass
    return render_template('index.html', error="Failed to fetch price", price=None)

@app.route('/top')
def top_coins():
    try:
        res = requests.get("https://api.coingecko.com/api/v3/coins/markets",
                           params={"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10})
        res.raise_for_status()
        return jsonify(res.json())
    except:
        return jsonify([])

@app.route('/history/<crypto>/<currency>')
def get_price_history(crypto, currency):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart"
        params = {"vs_currency": currency, "days": "7"}
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()

        prices = data.get("prices", [])
        labels = [datetime.datetime.fromtimestamp(p[0] / 1000).strftime('%d %b') for p in prices]
        values = [round(p[1], 2) for p in prices]

        return jsonify({"labels": labels, "values": values})
    except:
        return jsonify({"labels": [], "values": []})

@app.route('/sentiment')
def sentiment():
    try:
        res = requests.get("https://api.alternative.me/fng/")
        res.raise_for_status()
        data = res.json()["data"][0]
        return jsonify({
            "value": data["value"],
            "classification": data["value_classification"],
            "timestamp": data["timestamp"]
        })
    except:
        return jsonify({"value": "NA", "classification": "Unknown", "timestamp": ""})

if __name__ == '__main__':
    app.run(debug=True)
