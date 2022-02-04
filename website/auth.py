from flask import Blueprint, render_template, request, flash, redirect,url_for, session
from sqlalchemy.sql import func
from .models import Users, Codes
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .helper import *
from .send_sms import send_sms_code, send_email_code
from flask_login import login_user, login_required, logout_user, current_user
import pickle, os
from dotenv import load_dotenv
load_dotenv()

auth = Blueprint('auth', __name__)

# get a recovery code from the database. (password recovery)
def generate_auth_codes() -> int:
    code_1 = Codes.query.order_by(func.random()).first().auth_code
    code_2 = Codes.query.order_by(func.random()).first().auth_code
    return code_1, code_2


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


@auth.route("/password_recovery", methods=['GET','POST'])
def password_recovery():

    if request.method == 'POST':
        email = request.form.get('email')
        user = Users.query.filter_by(email=email).first()

        if user:
            email_verification_code, sms_verification_code = generate_auth_codes()
            send_email_code(user.email, email_verification_code)
            send_sms_code('+19492856292', sms_verification_code)
            
            session['email_verification_code'] =  email_verification_code
            session['sms_verification_code'] = sms_verification_code

            return redirect(url_for('auth.sms_verification'))
        else:
            flash('Email does not exist.', category='error')

    return render_template('password_recovery.html', user=current_user)


@auth.route("/sms_verification/", methods=['GET','POST'])
def sms_verification():

    email_verification_code = session.get('email_verification_code',None)
    sms_verification_code = session.get('sms_verification_code', None)
    # get form data, compare to session data
    if request.method == 'POST':
        user_input_email_code = request.form.get('email_code')
        user_input_sms_code = request.form.get('sms_code')

        if int(user_input_email_code) == email_verification_code and int(user_input_sms_code) == sms_verification_code:
            return redirect(url_for('auth.change_password'))
        else:
            flash('Incorrect recovery codes', category='error')


    return render_template('sms_verification.html', user=current_user,)


@auth.route("/change_password", methods=['GET','POST'])
def change_password():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 == password2:
            user = Users.query.filter_by(email=email).first()
            if user:
                user.password = generate_password_hash(password1, method='sha256')
                return redirect(url_for('auth.login'))
            else:
                flash('Email does not exist.', category='error')
        else:
            flash('Passwords must match', category='error')


    return render_template('change_password.html', user=current_user)


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
            # data points look like: [('12-28-2021', 38523.39)] where (date,total portfolio value)
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

