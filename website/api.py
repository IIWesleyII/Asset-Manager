from flask import Flask
from flask import  Blueprint
from .models import Users, Assets
from .finance import *

api = Blueprint('api',__name__)

@api.route('/api/v1/')
def home_api():
    return '<h1>Asset Manager Api</h1>'

@api.route('/api/v1/user', methods = ['GET'])
def get_users():
    users = Users.query.all()
    output = []
    if users:
        for user in users:
            user_data = {'name' : f'{user.f_name} {user.l_name}',
            'email' : user.email,
            'phone_number': user.phone_number,
            'country' : user.country,
            'base_currency' : user.base_currency,
            'is_premium' : user.is_premium,
            'total_asset_value': user.total_asset_value
            }
            output.append(user_data)
        return {'users': output}, 200
    else:
        return {'error':'users not found'} , 404

@api.route('/api/v1/user/<int:id>', methods = ['GET'])
def get_user_by_id(id):
    user = Users.query.get(id)
    if user:
        return {'name' : f'{user.f_name} {user.l_name}',
            'email' : user.email,
            'phone_number': user.phone_number,
            'country' : user.country,
            'base_currency' : user.base_currency,
            'is_premium' : user.is_premium,
            'total_asset_value': user.total_asset_value
            }
    else:
        return {'error':'user not found'} ,404

@api.route('/api/v1/user/email/<string:email>', methods = ['GET'])
def get_user_by_email(email):
    user = Users.query.filter_by(email=email).first()
    if user:
        return {'name' : f'{user.f_name} {user.l_name}',
            'email' : user.email,
            'phone_number': user.phone_number,
            'country' : user.country,
            'base_currency' : user.base_currency,
            'is_premium' : user.is_premium,
            'total_asset_value': user.total_asset_value
            }
    else:
        return {'error':'user not found'} ,404

@api.route('/api/v1/user/country/<string:country>', methods = ['GET'])
def get_users_by_country(country):
    users = Users.query.filter_by(country=country)
    output = []
    for user in users:
        user_data = {'name' : f'{user.f_name} {user.l_name}',
            'email' : user.email,
            'phone_number': user.phone_number,
            'country' : user.country,
            'base_currency' : user.base_currency,
            'is_premium' : user.is_premium,
            'total_asset_value': user.total_asset_value
            }
        output.append(user_data)
    if len(output) > 0:
        return {'users':output}, 200
    else:
        return {'error':'Country has no users'} ,404

@api.route('/api/v1/user/premium', methods = ['GET'])
def get_premium_users():
    users = Users.query.filter_by(is_premium=True)
    output = []
    for user in users:
        user_data = {'name' : f'{user.f_name} {user.l_name}',
            'email' : user.email,
            'phone_number': user.phone_number,
            'country' : user.country,
            'base_currency' : user.base_currency,
            'is_premium' : user.is_premium,
            'total_asset_value': user.total_asset_value
            }
        output.append(user_data)
    if len(output) > 0:
        return {'users':output}, 200
    else:
        return {'error':'No premium users'} ,404

@api.route('/api/v1/user/richest', methods = ['GET'])
def get_richest_user():
    users = Users.query.all()

    if users:
        richest_user = ''
        richest_user_asset_value = 0.0
        for user in users:
            print(richest_user_asset_value)
            if float(user.total_asset_value) > float(richest_user_asset_value):
                richest_user = user
                richest_user_asset_value = user.total_asset_value

        return {'user': {'name' : f'{richest_user.f_name} {richest_user.l_name}',
            'email' : richest_user.email,
            'phone_number': richest_user.phone_number,
            'country' : richest_user.country,
            'base_currency' : richest_user.base_currency,
            'is_premium' : richest_user.is_premium,
            'total_asset_value': richest_user.total_asset_value
            }}, 200
    else:
        return {'error':'No users found'} ,404

@api.route('/api/v1/user/total-assets', methods = ['GET'])
def get_total_asset_value_of_users():
    users = Users.query.all()
    total = 0.0
    if users:
        for user in users:
            total += float(user.total_asset_value)

        return {'total_assets': total, 'base_currency': 'Dollars'}, 200
    else:
        return {'error':'No users found'} ,404



