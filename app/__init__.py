from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate

migrate = Migrate()
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    migrate.init_app(app, db)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app