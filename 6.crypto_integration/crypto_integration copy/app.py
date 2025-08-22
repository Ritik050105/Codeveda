from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    price = None
    error = None
    crypto_name = ''
    currency = ''

    if request.method == 'POST':
        crypto_name = request.form['crypto'].lower().strip()
        currency = request.form['currency'].lower().strip()
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": crypto_name, "vs_currencies": currency}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if crypto_name in data and currency in data[crypto_name]:
                price = data[crypto_name][currency]
            else:
                error = "Invalid cryptocurrency or currency code."
        except Exception as e:
            error = f"API Error: {str(e)}"

    return render_template("index.html", price=price, error=error,
                           crypto=crypto_name, currency=currency)

if __name__ == '__main__':
    app.run(debug=True)
