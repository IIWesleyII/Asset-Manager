from flask import Blueprint,render_template, request, flash, redirect,url_for
from flask_login import  login_required,  current_user
from sqlalchemy.sql.functions import user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Users, Assets

import datetime
# x = datetime.datetime.now()

transaction = Blueprint('transaction', __name__)

# remove chars from asset_price
def change_price(asset_price)->float:
    new_price = ''
    for ch in asset_price:
        if ch.isdigit() or ch == '.':
            new_price += ch
    return float(new_price)


@transaction.route('/transaction/buy/<string:asset_name>/<string:asset_price>/<string:asset_type>',methods=['GET','POST'])
@login_required
def buy(asset_name,asset_price, asset_type):
    if request.method == 'POST':
        asset_qty = request.form.get('qty')
        credit_card_number = request.form.get('credit_card_number')

        new_price = change_price(asset_price)
        purchase_value =new_price*int(asset_qty)
        if check_password_hash(current_user.payment_info, credit_card_number):
            try:
                user = Users.query.get_or_404(current_user.id)
            except:
                raise Exception('User does not exist.')

            # update curr user total_asset value by purchase value
            if current_user.total_asset_value:
                user.total_asset_value = float(current_user.total_asset_value) +  purchase_value
            else:
                 user.total_asset_value = purchase_value

            new_asset = Assets(asset_name=asset_name, asset_type =asset_type, asset_qty=asset_qty,
            asset_price=asset_price, date=datetime.datetime.now(),user_id= current_user.id)

            db.session.add(new_asset)
            db.session.commit()

            flash("Purchase successful", category="success")

            return render_template("market.html", user=current_user)
        else:
            flash("Invalid credit card number", category="error")

    return render_template("buy.html", user=current_user, asset_name=asset_name, asset_price=asset_price, asset_type=asset_type)


@transaction.route('/transaction/sell/<string:asset_name>/<string:asset_price>/<string:asset_type>',methods=['GET','POST'])
@login_required
def sell(asset_name,asset_price, asset_type):
    display_total_qty = 0
    try:
        assets = Assets.query.filter(Assets.user_id==current_user.id)
    except:
        raise Exception('Assets does not exist.')
    '''
    Display the amount of the asset the current user has
    '''
   
    if assets:
        for asset in assets:
            if asset.asset_name == asset_name:
                display_total_qty += int(asset.asset_qty)
        if display_total_qty > 0:
            flash(f"You have {display_total_qty} {asset_name} to sell.", category="success")
        else:
            flash(f"You currently do not have any {asset_name} to sell.", category="error")
    else:
        flash(f"You currently do not have any {asset_name} to sell.", category="error")
    
    '''
    Subtract the sell amount from the current user's total asset value
    '''
    if request.method == 'POST':
        try:
            asset_qty = int(request.form.get('qty'))
        except:
            flash(f"qty must be integer", category="error")

        new_price = change_price(asset_price)
        try:
            user = Users.query.get_or_404(current_user.id)
        except:
            raise Exception('User does not exist.')
        if user.total_asset_value:
            new_total_asset_value = float(user.total_asset_value)
            for i in range(int(asset_qty)):
                if new_total_asset_value <0:
                    flash("You do not have enough assets to sell", category="error")
                    break
                else:
                    new_total_asset_value -= new_price

            if new_total_asset_value >=0:
                user.total_asset_value = new_total_asset_value
                flash(f"{asset_qty} sold!", category="success")
        '''
        change asset qty in the Assets table
        '''
        for asset in assets:
            if int(asset.asset_qty) < asset_qty:
                asset_qty -= int(asset.asset_qty)
                asset.asset_qty = 0
            elif int(asset.asset_qty) >= asset_qty:
                 asset.asset_qty = int(asset.asset_qty) -asset_qty
                 break
            
        db.session.commit()

               
    return render_template("sell.html", user=current_user, asset_name=asset_name, asset_price=asset_price, asset_type=asset_type)