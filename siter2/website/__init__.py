from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_cors import CORS
from os import path

db = SQLAlchemy()
DB_NAME = "database"

#initialize website:

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config['SECRET_KEY'] = 'julioindapocket'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///database'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .views import views
    from .auth import auth
    from .stores import stores

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(stores, url_prefix='/')

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    db.create_all(app=app)

    return app