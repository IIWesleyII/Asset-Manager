from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Assets(db.Model):
    asset_id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(100))
    asset_type = db.Column(db.String(100))
    asset_qty = db.Column(db.String(100))
    asset_price = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    f_name = db.Column(db.String(100))
    l_name = db.Column(db.String(100))
    country = db.Column(db.String(100))
    password = db.Column(db.String(100))
    base_currency = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    two_factor_auth_type = db.Column(db.String(100))
    is_premium = db.Column(db.Boolean, default=False)
    payment_info = db.Column(db.Integer)
    total_asset_value = db.Column(db.String(100))
    asset_chart_plot_data = db.Column(db.LargeBinary)
    assets = db.relationship('Assets')
    
