from flask import Blueprint,render_template, request, flash, redirect,url_for
from flask_login import  login_required,  current_user
from sqlalchemy.sql.functions import user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Users, Assets
from .finance import *
import datetime, pickle

transaction = Blueprint('transaction', __name__)


@transaction.route('/transaction/buy/<string:asset_name>/<string:asset_price>/<string:asset_type>',methods=['GET','POST'])
@login_required
def buy(asset_name,asset_price, asset_type):
    ''''
    buy()
    Function allows for users to buy assets using their payment type
        i) accepts and authenticates payment info
        ii) updates user's asset balance
        iii) updates user's portfolio graph
        iv) create's new asset for user
    '''
    asset_qty = 0
    if request.method == 'POST':
        try:
            asset_qty = float(request.form.get('qty'))
        except:
            flash("Invalid quantity", category="error")
            
        if type(asset_qty) == float:
            credit_card_number = request.form.get('credit_card_number')
                
            # change_price, defined in .finance, converts and strips chars from the string price into a float
            new_price = change_price(asset_price)
            purchase_value =new_price*float(asset_qty)
            if check_password_hash(current_user.payment_info, credit_card_number):
                try:
                    user = Users.query.get_or_404(current_user.id)
                except:
                    raise Exception('User does not exist.')
                    
                # update curr user total_asset value by purchase value
                if current_user.total_asset_value:
                    user.total_asset_value = round(float(current_user.total_asset_value) +  purchase_value,3)
                else:
                    user.total_asset_value = round(purchase_value,3)

                #update current user with new plot point for the totatal asset value over time graph
                asset_chart_plot_data = generate_chart_plot_data(pickle.loads(user.asset_chart_plot_data))
                user.asset_chart_plot_data = pickle.dumps(asset_chart_plot_data)
                x = pickle.loads(user.asset_chart_plot_data)
                asset = Assets.query.filter(Assets.user_id==current_user.id, Assets.asset_name==asset_name).first()

                if asset:
                    asset.asset_qty = float(asset.asset_qty) + float(asset_qty)
                    asset.asset_price = new_price
                    asset.date = datetime.datetime.now()
                else:
                    new_asset = Assets(asset_name=asset_name, asset_type =asset_type, asset_qty=asset_qty,
                    asset_price=new_price, date=datetime.datetime.now(),user_id=current_user.id)
                    db.session.add(new_asset)
                db.session.commit()
                flash("Purchase successful", category="success")
                return render_template("market.html",user=current_user)
            else:
                flash("Invalid credit card number", category="error")

    return render_template("buy.html", user=current_user, asset_name=asset_name, asset_price=asset_price, asset_type=asset_type)


@transaction.route('/transaction/sell/<string:asset_name>/<string:asset_price>/<string:asset_type>',methods=['GET','POST'])
@login_required
def sell(asset_name,asset_price, asset_type):
    ''''
    sell()
    Function allows for users to sell assets using their payment type
        i) check if user has enough assets to sell
        ii) updates user's asset balance
        iii) updates user's portfolio graph
        iv) updates asset for user
    '''
    asset_qty = 0
    display_total_qty = 0
    try:
        curr_asset_obj = Assets.query.filter(Assets.user_id==current_user.id,Assets.asset_name==asset_name).first()
    except:
        raise Exception('Asset does not exist.')

    #Display the amount of the asset the current user has
    if curr_asset_obj:
        display_total_qty += float(curr_asset_obj.asset_qty)
        if display_total_qty > 0:
            flash(f"You have {display_total_qty} {asset_name} to sell.", category="success")
        else:
            flash(f"You currently do not have any {asset_name} to sell.", category="error")
    else:
        flash(f"You currently do not have any {asset_name} to sell.", category="error")
    
    #Subtract the sell amount from the current user's total asset value
    if request.method == 'POST':
        try:
            asset_qty = float(request.form.get('qty'))
        except:
            flash(f"qty must be integer", category="error")

        if type(asset_qty) == float:
            new_price = change_price(asset_price)
            try:
                user = Users.query.get_or_404(current_user.id)
            except:
                raise Exception('User does not exist.')

            if user.total_asset_value:
                new_total_asset_value = float(user.total_asset_value)

                #change asset qty in the Assets table and change user total_asset_value
                if float(curr_asset_obj.asset_qty) >= asset_qty and asset_name==curr_asset_obj.asset_name:
                    curr_asset_obj.asset_qty = round(float(curr_asset_obj.asset_qty) - asset_qty,3)
                    new_total_asset_value -= (new_price * asset_qty)

                    flash(f"{asset_qty} sold!", category="success")

                    if new_total_asset_value >=0:
                        user.total_asset_value = round(new_total_asset_value,3)
                        #update current user with new plot point for the total asset value over time graph
                        asset_chart_plot_data = generate_chart_plot_data(pickle.loads(user.asset_chart_plot_data))
                        user.asset_chart_plot_data = pickle.dumps(asset_chart_plot_data)

                else:
                    flash(f"You currently do not have enough {asset_name} to sell.", category="error")
    
            db.session.commit()
            return render_template("market.html", user=current_user,asset_name=asset_name, asset_price=asset_price, asset_type=asset_type)
               
    return render_template("sell.html", user=current_user, asset_name=asset_name, asset_price=asset_price, asset_type=asset_type)