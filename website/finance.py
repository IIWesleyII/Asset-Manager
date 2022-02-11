import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
from datetime import datetime
from flask_login import current_user

from dotenv import load_dotenv
load_dotenv()
'''
This file contains 
- functions to get outside financial API data
- convert currency and assets
- generate json files of current asset prices

'''

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
    if base_currency == 'Dollars':
        conversion_factor = 1
        currency_symbol = '$'
    elif base_currency == 'Euros':
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
def get_crypto_prices():
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
Get commodity api data from commodities-api
https://commodities-api.com/documentation

'''

def get_commodity_prices():
    api_key = os.getenv('COMMODITIES_API_KEY')
    response = requests.get('https://commodities-api.com/api/latest?access_key='+api_key)
    
    with open('commodity_prices.json', 'a', encoding='utf-8') as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
    if response.status_code != 200:
        print(response.status_code)
'''
Get stock api data from polygon
https://polygon.io/docs/stocks/getting-started

'''

def get_stock_prices():
    api_key = os.getenv('STOCKS_API_KEY')
    response = requests.get('https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2021-12-22?adjusted=true&apiKey='+api_key)
    with open('stock_prices.json', 'a', encoding='utf-8') as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
    if response.status_code != 200:
        print(response.status_code)

'''
Send API Data to JSON files
print_commodity_prices()
print_crypto_prices()
print_stock_prices()

'''

'''
GET PRICES FOR Crytpocurrency
returns data in the form of a list of tuples
[('Bitcoin', 48705.177689493146), (...)]

'''
def list_crypto_prices()-> list:
    data = {}
    prices = []
    with open('website\prices\crypto_prices.json','r', encoding="utf8") as f:
        data = json.load(f)

    # current_user.base_currency is a string ex. ('Dollar','Euro',...)
    currency_multiplier,currency_symbol = currency_converter(current_user.base_currency)
    
    for i in range(len(data['data'])):
        name = data['data'][i]['name']
        # round price to 3 decimal places
        price = round(float(data['data'][i]['quote']['USD']['price']) * currency_multiplier, 3)

        if currency_symbol == '€' or currency_symbol == '$':
            price = f'{currency_symbol}{price}'
        else:
            price = f'{price} {currency_symbol}'
        prices.append((name,price,'cryptocurrency'))

    return prices

'''
GET PRICES FOR COMMODITIES
returns data in the form of a list of tuples
[('JFH', 705.2), (...)]
'''
def list_commodity_prices()-> list:
    data = {}
    prices = []
    with open('website\prices\commodity_prices.json','r', encoding="utf8") as f:
        data = json.load(f)

    # current_user.base_currency is a string ex. ('Dollar','Euro',...)
    currency_multiplier,currency_symbol = currency_converter(current_user.base_currency)

    for key, val in data['data']['rates'].items():
        name = key
        # round price to 3 decimal places
        price = round(val * currency_multiplier,3)

        if currency_symbol == '€' or currency_symbol == '$':
            price = f'{currency_symbol}{price} per unit'
        else:
            price = f'{price} {currency_symbol} per unit'

        prices.append((name,price, 'commodity'))

    return prices


'''
GET PRICES FOR STOCKS
returns data in the form of a list of tuples
[('AAPL', 178.2), (...)]
'''
def list_stock_prices()-> list:
    data = {}
    prices = []
    with open('website\prices\stock_prices.json','r', encoding="utf8") as f:
        data = json.load(f)

    # current_user.base_currency is a string ex. ('Dollar','Euro',...)
    currency_multiplier,currency_symbol = currency_converter(current_user.base_currency)
    
    for i in range(len(data['results'])):
        name = data['results'][i]['T']
        # round price to 3 decimal places
        price = round(data['results'][i]['h'] * currency_multiplier, 3)

        if currency_symbol == '€' or currency_symbol == '$':
            price = f'{currency_symbol}{price}'
        else:
            price = f'{price} {currency_symbol}'

        prices.append((name,price,'stock'))

    return prices


'''
GET PRICES FOR ALTERNATIVE ASSETS
 - alternative assets such as cars, luxury goods, housing, etc
returns data in the form of a list of tuples
[('WATCH id# 102938', 1078.2), (...)]
'''
def list_alternative_prices()->list:
    inpt_lst = [("ROLEX watch (Cosmograph Daytona Chronograph Automatic Men's Oysterflex Watch 116518BKCSR)", 56000.00),("House #8293", 976883.00)]
    prices = []

    # current_user.base_currency is a string ex. ('Dollar','Euro',...)
    currency_multiplier,currency_symbol = currency_converter(current_user.base_currency)

    for i in range(len(inpt_lst)):
        name = inpt_lst[i][0]
        # round price to 3 decimal places
        price = round(inpt_lst[i][1] * currency_multiplier,3)

        if currency_symbol == '€' or currency_symbol == '$':
            price = f'{currency_symbol}{price}'
        else:
            price = f'{price} {currency_symbol}'

        prices.append((name,price,'alternative'))

    return prices

'''
- here I will need to write functions to get curr price of one particular asset,  for each asset class
- write a refresh_prices function
'''
def refresh_prices():
    get_alternative_prices()



# remove chars from asset_price
def change_price(asset_price)->float:
    new_price = ''
    for ch in asset_price:
        if ch.isdigit() or ch == '.':
            new_price += ch
    return float(new_price)

# find the total evaluation of a users assests
def find_total_asset_value(assets) -> float:
    total_value = 0.0
    for asset in assets:
        if float(asset.asset_price) > 0 and int(asset.asset_qty) > 0:
            total_value += int(asset.asset_qty) * float(asset.asset_price)

    return round(total_value,3)

# append to the list of asset changes over time
def generate_chart_plot_data(lst=[])->list:
    if lst == []:
        return [(f'{datetime.now().ctime()}',0.0)]
    else:
        lst.append((f'{datetime.now().ctime()}',current_user.total_asset_value))
        return lst
