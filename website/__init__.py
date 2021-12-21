from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()
DB_NAME = os.getenv('DB_NAME') 

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    
    db.init_app(app)

    #blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # create db
    from .models import Users, Assets

    create_database(app)
    
    return app

def create_database(app):
    if not os.path.exists('website/'+ DB_NAME):
        db.create_all(app=app)
        print('Created_DB')
