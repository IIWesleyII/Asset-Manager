from datetime import datetime
from flask_login import current_user

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