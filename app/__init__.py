from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)

    # Model
    from app.model import user, dosen, mahasiswa

    # Controller
    from .controller.api.routes import api
    from .controller.auth.routes import auth
    from .controller.site.routes import site
    from .controller.errors.handlers import errors

    # Blueprint
    app.register_blueprint(api)
    app.register_blueprint(auth)
    app.register_blueprint(site)
    app.register_blueprint(errors)

    return app