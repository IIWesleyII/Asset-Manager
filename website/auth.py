from flask import Blueprint, render_template, request, flash, redirect,url_for
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .helper import *
from flask_login import login_user, login_required, logout_user, current_user
import pickle
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.portfolio'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        f_name = request.form.get('firstName')
        l_name = request.form.get('lastName')
        country = request.form.get('country')
        base_currency = request.form.get('base_currency')
        two_factor_auth_type = request.form.get('two_factor_auth_type')
        phone_number = request.form.get('phone_number')
        payment_info = request.form.get('payment_info')
        password_1 = request.form.get('password1')
        password_2 = request.form.get('password2')

        user = Users.query.filter_by(email=email).first()

        if user:
            flash("Email already exists.", category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(f_name) == 0:
            flash('First Name cannot be empty.', category='error')
        elif len(l_name) == 0:
            flash('Last Name cannot be empty.', category='error')
        elif len(country) == 0:
            flash('Country cannot be empty.', category='error')
        elif len(base_currency) == 0:
            flash('Choose a base currency.', category='error')
        elif len(two_factor_auth_type) == 0:
            flash('Choose a type of two factor authentication.', category='error')
        elif len(phone_number) < 7 or phone_number.isdigit() == False:
            flash('Phone number bust be 10 numbers', category='error')
        elif len(payment_info) != 16 or payment_info.isdigit() == False:
            flash('Enter a correct 16 digit Credit card number.', category='error')    
        elif password_1 != password_2:
            flash('Password\'s do not match.', category='error')
        elif len(password_1) < 7:
            flash('Password must be at least 8 characters long.', category='error')
        else:
            # plot first point on asset graph with beginning data
            # then pickle list to be saved in database
            asset_chart_plot_data = pickle.dumps(generate_chart_plot_data([]))

            new_user = Users(email=email, f_name=f_name, l_name=l_name, 
                country=country, base_currency=base_currency, two_factor_auth_type=two_factor_auth_type,
                phone_number=phone_number,payment_info=generate_password_hash(payment_info, method='sha256'),
                password=generate_password_hash(password_1, method='sha256'), asset_chart_plot_data = asset_chart_plot_data)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.portfolio'))


    return render_template('sign_up.html',user=current_user)

