import os
from flask import Flask
from app.config import config
from app.extensions import db, migrate, mail, limiter

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config["default"]))

    # Bind extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    limiter.init_app(app)

    # Import models package so metadata registers with the unified db instance
    from app import models

    # Register Blueprints
    from app.views.main_routes import main_bp
    from app.views.form_routes import form_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(form_bp, url_prefix="/forms")

    return app