from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

