from flask import Blueprint,render_template, request, flash, redirect,url_for
from flask_login import  login_required,  current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

import datetime
# x = datetime.datetime.now()

transaction = Blueprint('transaction', __name__)

@transaction.route('/transaction/buy/<string:asset_name>/<string:asset_price>',methods=['GET','POST'])
@login_required
def buy(asset_name,asset_price):
    if request.method == 'POST':
        qty = request.form.get('qty')
        credit_card_number = request.form.get('credit_card_number')

        if check_password_hash(current_user.payment_info, credit_card_number):
            pass

    return render_template("buy.html", user=current_user, asset_name=asset_name, asset_price=asset_price)

@transaction.route('/transaction/sell/<string:asset_name>/<string:asset_price>',methods=['GET','POST'])
@login_required
def sell(asset_name,asset_price):
    return render_template("sell.html", user=current_user, asset_name=asset_name, asset_price=asset_price)