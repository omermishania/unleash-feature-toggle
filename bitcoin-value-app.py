# imports
from flask import Flask, request, abort
from UnleashClient import UnleashClient
import requests
import json

# Returns the feature toggle's state from Unleash API
def feature_toggle_on():
    client = UnleashClient(url="http://baruch.cloudlet-dev.com:4242/api", app_name="bitcoin-info", custom_headers={'Authorization': '*:*.7a42d8fc36c05a428c5afb6648678653a1848fea5bfc25c8e0920f76'})
    client.initialize_client()
    toggle_state  = client.is_enabled("your-toggle-name")
    return toggle_state


app = Flask(__name__)


@app.route("/usd")
# Returns the value of Bitcoin in USD on server-ip/usd
def usd_currency():
    currency_code = 'USD'

    bitcoin_info = requests.get('https://api.coinbase.com/v2/prices/spot?currency='+currency_code).text # get Bitcoin info in USD from coinbase API
    bitcoin_info = json.loads(bitcoin_info)
    bitcoin_price = bitcoin_info['data']['amount'] # get only bitcoin price in USD
    return f'Current bitcoin price in {currency_code} is: {bitcoin_price}'


@app.route("/")
# In case the feature toggle is on, returns the value of Bitcoin in the chosen currency. If it's off, returns 404
def home():
    if feature_toggle_on():
        currency_code = request.args.get('currency')
        bitcoin_info = requests.get('https://api.coinbase.com/v2/prices/spot?currency='+currency_code).text # get Bitcoin info in the chosen currency from coinbase API
        bitcoin_info = json.loads(bitcoin_info)
        if 'errors' in bitcoin_info:
            return f'{currency_code} Currency does not exist'
        bitcoin_price = bitcoin_info['data']['amount'] # get only bitcoin price
        return f'Current bitcoin price in {currency_code} is: {bitcoin_price}'
    else:
        abort(404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
