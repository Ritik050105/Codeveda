from flask import Flask, render_template, request, jsonify
import requests
import datetime
import requests_cache
requests_cache.install_cache('crypto_cache', expire_after=60)

app = Flask(__name__)

COIN_LIST_URL = "https://api.coingecko.com/api/v3/coins/list"
coin_list = []

# Fetch coin list at startup
def load_coin_list():
    global coin_list
    res = requests.get(COIN_LIST_URL)
    if res.ok:
        coin_list = res.json()

@app.route('/', methods=['GET', 'POST'])
def index():
    price = None
    error = None
    converted = None
    crypto_name = ''
    currency = ''

    if request.method == 'POST':
        crypto_name = request.form['crypto'].lower().strip()
        currency = request.form['currency'].lower().strip()
        target_crypto = request.form.get('target_crypto', '').lower().strip()

        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": crypto_name, "vs_currencies": currency}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if crypto_name in data and currency in data[crypto_name]:
                price = data[crypto_name][currency]

                # Crypto-to-crypto conversion
                if target_crypto:
                    target_params = {"ids": target_crypto, "vs_currencies": currency}
                    t_data = requests.get(url, params=target_params).json()
                    if target_crypto in t_data and currency in t_data[target_crypto]:
                        target_price = t_data[target_crypto][currency]
                        converted = round(price / target_price, 6)
            else:
                error = "Invalid crypto or currency."
        except Exception as e:
            error = f"API Error: {str(e)}"

    return render_template("index.html", price=price, error=error,
                           crypto=crypto_name, currency=currency,
                           coin_list=coin_list, converted=converted)

@app.route('/history/<crypto>/<currency>')
def get_price_history(crypto, currency):
    try:
        res = requests.get(f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart",
                           params={"vs_currency": currency, "days": "7"})
        res.raise_for_status()
        data = res.json()
        prices = data.get("prices", [])
        labels = [datetime.datetime.fromtimestamp(p[0] / 1000).strftime('%d %b') for p in prices]
        values = [round(p[1], 2) for p in prices]
        return jsonify({"labels": labels, "values": values})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/top')
def top_coins():
    try:
        res = requests.get("https://api.coingecko.com/api/v3/coins/markets",
                           params={"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10})
        data = res.json()
        return jsonify(data)
    except:
        return jsonify([])

@app.route('/sentiment')
def sentiment():
    try:
        res = requests.get("https://api.alternative.me/fng/?limit=1")
        data = res.json()
        return jsonify(data["data"][0])
    except:
        return jsonify({"value": "NA", "value_classification": "Unknown"})

if __name__ == "__main__":
    load_coin_list()
    app.run(debug=True)
