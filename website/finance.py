from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
from flask_login import  login_required,  current_user

from dotenv import load_dotenv
load_dotenv()

'''
CURRENCY CONVERTER
- For now will be hardcoded, in the future make api call and get proper currency conversions
    hardcoded 12/22/2021 7:47 AM
- finds conversion factor of the passed in base_currency
- $ * (Euro factor) = value in euros
'''
def currency_converter(base_currency):
    conversion_factor = 0
    currency_symbol = ''
    if base_currency == 'Dollar':
        conversion_factor = 1
        currency_symbol = '$'
    elif base_currency == 'Euro':
        conversion_factor = 0.88
        currency_symbol = '€'
    elif base_currency == 'Ether':
        conversion_factor = 0.00025
        currency_symbol = 'Ether'
    elif base_currency == 'Bitcoin':
        conversion_factor = 0.000020
        currency_symbol = 'Bitcoin'
    elif base_currency == 'Ada':
        conversion_factor = 0.75
        currency_symbol = 'Ada' 
    else:
        raise ValueError(f"Input must be valid currency. Currency name give:{base_currency}")
    return conversion_factor, currency_symbol


'''
coinmarketcap api functions
Get api crypto data from coinmarketcap
https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyListingsLatest
'''
def print_crypto_prices():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'5000',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY':  os.getenv('COIN_MARKET_CAP_API_KEY'),
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        with open('crypto_prices.json', 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

'''
GET CRYPTO PRICES
returns data in the form of a list of tuples
[('Bitcoin', 48705.177689493146), (...)]

'''
def get_crypto_prices()-> list:
    data = {}
    prices = []
    with open('website\prices\crypto_prices.json','r', encoding="utf8") as f:
        data = json.load(f)

    # current_user.base_currency is a string ex. ('Dollar','Euro',...)
    currency_multiplier,currency_symbol = currency_converter(current_user.base_currency)
    
    for i in range(len(data['data'])):
        name = data['data'][i]['name']
        price = round(float(data['data'][i]['quote']['USD']['price']),3) * currency_multiplier

        if currency_symbol == '€' or currency_symbol == '$':
            price = f'{currency_symbol}{price}'
        else:
            price = f'{price} {currency_symbol}'
        prices.append((name,price))
    return prices




