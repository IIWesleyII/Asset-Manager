from flask import Blueprint,render_template, request, flash, redirect,url_for
from flask_login import  login_required,  current_user


from .finance import *
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)


@views.route('/portfolio')
@login_required
def portfolio():
    return render_template("portfolio.html", user=current_user)


@views.route('/market',methods=['GET','POST'])
@login_required
def market():
    if request.method == 'POST':
        asset_type = request.form.get('asset_type')
        if asset_type == '':
            pass
        elif asset_type == 'cryptocurrency':
            return render_template("market.html", crypto_prices = get_crypto_prices(), user=current_user)
        elif asset_type == 'commodities':
            return render_template("market.html", commodity_prices = get_commodity_prices(), user=current_user)
        elif asset_type == 'stocks':
            pass
        elif asset_type == 'alternative':
            pass
        else:
            raise ValueError('Choose valid asset type.')
    return render_template("market.html", user=current_user)

@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)
