from flask import Flask
from flask_cors import CORS
from flask_wtf import CSRFProtect
from flask_login import LoginManager

from web3 import Web3

from config import WEB3_PROVIDER

from utils.database import engine
from utils.models import Base

csrf: CSRFProtect = CSRFProtect()
w3: Web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))


def setup_db():
    Base.metadata.create_all(bind=engine)


def create_app() -> Flask:
    app = Flask(__name__, static_url_path="/assets", static_folder="assets")
    CORS(app, allow_origin="*")
    app.config.from_pyfile("config.py")

    global csrf
    csrf.init_app(app)

    setup_db()

    login_manager = LoginManager()
    login_manager.init_app(app)

    with app.app_context():

        @login_manager.user_loader
        def load_user(address: str):
            from utils.database import create_session
            from utils.models import User

            session = create_session()
            return session.query(User).filter(User.address == address).first()

        @login_manager.unauthorized_handler
        def _unauthorized():
            from flask import redirect, url_for, flash

            flash("You must be logged in to access this page.", "warning")
            return redirect(url_for("meta._index"))

        @app.template_filter("format")
        def _format(dt):
            return dt.strftime("%Y-%m-%d")

        @app.template_filter("truncate")
        def _truncate(text, length=100):
            return text[:length] + "..." if len(text) > length else text

        @app.template_filter("markdown")
        def _markdown(text):
            from markdown import markdown

            return markdown(text)

        @app.before_request
        def check_username():
            from flask import request, redirect, url_for
            from flask_login import current_user

            if request.endpoint in ["auth._username", "auth._logout", "static"]:
                return

            if current_user.is_authenticated and not current_user.username:
                return redirect(url_for("auth._username"))

    from blueprints.app import app_bp
    from blueprints.auth import auth_bp
    from blueprints.meta import meta_bp
    from blueprints.posts import posts_bp
    from blueprints.tips import tips_bp

    app.register_blueprint(app_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(meta_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(tips_bp)

    csrf.exempt("blueprints.auth.routes._message")
    csrf.exempt("blueprints.auth.routes._verify")
    csrf.exempt("blueprints.tips.routes._record")

    return app
