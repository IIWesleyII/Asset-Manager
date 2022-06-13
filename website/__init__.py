from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_login import LoginManager
load_dotenv()

db = SQLAlchemy()
DB_NAME = os.getenv('DB_NAME') 

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    
    db.init_app(app)

    #blueprints
    from .views import views
    from .auth import auth
    from .transaction import transaction
    from .api import api
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(transaction, url_prefix='/')
    app.register_blueprint(api, url_prefix='')
    
    # create db
    from .models import Users, Assets
    create_database(app)

    # init flask login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))
    
    return app

def create_database(app):
    if not os.path.exists('website/'+ DB_NAME):
        db.create_all(app=app)
        print('Created_DB')
