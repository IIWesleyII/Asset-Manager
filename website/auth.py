from flask import Blueprint, render_template, request, flash, redirect,url_for
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
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
        phone_number = request.form.get('phone_number')
        password_1 = request.form.get('password1')
        password_2 = request.form.get('password2')

        user = Users.query.filter_by(email=email).first()

        if user:
            flash("Email already exists.")
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(f_name) == 0:
            flash('First Name cannot be empty.', category='error')
        elif len(l_name) == 0:
            flash('Last Name cannot be empty.', category='error')
        # evntually make country dropdown menu
        elif len(country) == 0:
            flash('Country cannot be empty.', category='error')
        elif len(phone_number) < 7 or phone_number.isdigit() == False:
            flash('Phone number bust be 10 numbers', category='error')
        elif password_1 != password_2:
            flash('Password\'s do not match.', category='error')
        elif len(password_1) < 7:
            flash('Password must be at least 8 characters long.', category='error')
        else:
            new_user = Users(email=email, f_name=f_name, l_name=l_name, 
                country=country, phone_number=phone_number, password=generate_password_hash(password_1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.portfolio'))


    return render_template('sign_up.html',user=current_user)

