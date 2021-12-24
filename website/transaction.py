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
        assets = Assets.query.all()
    except:
        raise Exception('Assets does not exist.')
    if assets:
        for asset in assets:
            if asset.user_id == current_user.id:
                if asset.asset_name == asset_name:
                    display_total_qty += int(asset.asset_qty)
        if display_total_qty > 0:
            flash(f"You have {display_total_qty} {asset_name} to sell.", category="success")
        else:
            flash(f"You currently do not have any {asset_name} to sell.", category="error")
    else:
        flash(f"You currently do not have any {asset_name} to sell.", category="error")

    asset_qty = request.form.get('qty')
    new_price = change_price(asset_price)

    return render_template("sell.html", user=current_user, asset_name=asset_name, asset_price=asset_price, asset_type=asset_type)