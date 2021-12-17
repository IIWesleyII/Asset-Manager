from flask import Blueprint, render_template, request, flash


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET','POST'])
def login():

    return render_template('login.html')

@auth.route('/logout')
def logout():
    return '<p>logout</p>'

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        location = request.form.get('location')
        password_1 = request.form.get('password1')
        password_2 = request.form.get('password2')

        #input integrity check
        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) == 0:
            flash('First Name cannot be empty.', category='error')
        elif len(last_name) == 0:
            flash('Last Name cannot be empty.', category='error')
        # evntually make location a dropdown menu
        elif len(location) == 0:
            flash('Location cannot be empty.', category='error')
        elif password_1 != password_2:
            flash('Password\'s do not match.', category='error')
        elif len(password_1) < 7:
            flash('Password must be at least 8 characters long', category='error')
        else:
            #add user to db
            flash('Account created!', category='success')

    return render_template('sign_up.html')

