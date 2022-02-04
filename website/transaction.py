from flask import Blueprint,render_template, request, flash, redirect,url_for
from flask_login import  login_required,  current_user
from sqlalchemy.sql.functions import user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Users, Assets
from .helper import *
import datetime, pickle

transaction = Blueprint('transaction', __name__)

''''
buy()
Function allows for users to buy assets using their payment type
    i) accepts and authenticates payment info
    ii) updates user's asset balance
    iii) updates user's portfolio graph
    iv) create's new asset for user
'''
@transaction.route('/transaction/buy/<string:asset_name>/<string:asset_price>/<string:asset_type>',methods=['GET','POST'])
@login_required
def buy(asset_name,asset_price, asset_type):
    if request.method == 'POST':
        asset_qty = request.form.get('qty')
        credit_card_number = request.form.get('credit_card_number')
        
        if not asset_qty.isdigit():
            flash("Invalid quantity", category="error")
        else:

            # change_price, defined in .helper, converts and strips chars from the string price into a float
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
                    user.total_asset_value = round(purchase_value,3)
                #update current user with new plot point for the totatal asset value over time graph
                asset_chart_plot_data = generate_chart_plot_data(pickle.loads(user.asset_chart_plot_data))
                user.asset_chart_plot_data = pickle.dumps(asset_chart_plot_data)
                x = pickle.loads(user.asset_chart_plot_data)
                new_asset = Assets(asset_name=asset_name, asset_type =asset_type, asset_qty=asset_qty,
                asset_price=new_price, date=datetime.datetime.now(),user_id= current_user.id)
                db.session.add(new_asset)
                db.session.commit()
                flash("Purchase successful", category="success")
                return render_template("market.html",user=current_user)
            else:
                flash("Invalid credit card number", category="error")

    return render_template("buy.html", user=current_user, asset_name=asset_name, asset_price=asset_price, asset_type=asset_type)

''''
sell()
Function allows for users to sell assets using their payment type
    i) check if user has enough assets to sell
    ii) updates user's asset balance
    iii) updates user's portfolio graph
    iv) updates asset for user
'''
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
                user.total_asset_value = round(new_total_asset_value,3)

                #update current user with new plot point for the total asset value over time graph
                asset_chart_plot_data = generate_chart_plot_data(pickle.loads(user.asset_chart_plot_data))
                user.asset_chart_plot_data = pickle.dumps(asset_chart_plot_data)

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
        return render_template("market.html", user=current_user,asset_name=asset_name, asset_price=asset_price, asset_type=asset_type)
               
    return render_template("sell.html", user=current_user, asset_name=asset_name, asset_price=asset_price, asset_type=asset_type)