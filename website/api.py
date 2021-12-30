from flask import Flask
from flask import  Blueprint, render_template, request, jsonify
from .models import Users, Assets

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


