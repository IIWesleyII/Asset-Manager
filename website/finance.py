from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os


from dotenv import load_dotenv
load_dotenv()

def get_crypto_market_cap():
    return 'crypto'
def get_stock_market_cap():
    return 'stock'

'''
coinmarketcap api example
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
Get api crypto data from coinmarketcap
https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyListingsLatest

returns data in the form of a list of tuples
[('Bitcoin', 48705.177689493146), (...)]

'''
def get_crypto_prices()-> list:
    data = {}
    prices = []
    with open('website\crypto_prices.json','r', encoding="utf8") as f:
        data = json.load(f)
    
    for i in range(len(data['data'])):
        name = data['data'][i]['name']
        price = data['data'][i]['quote']['USD']['price']
        prices.append((name,price))

    return prices




