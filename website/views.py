from flask import Blueprint, render_template
from flask_login import  login_required,  current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)


@views.route('/portfolio')
@login_required
def portfolio():
    return render_template("portfolio.html", user=current_user)


@views.route('/market')
@login_required
def market():
    return render_template("market.html", user=current_user)
