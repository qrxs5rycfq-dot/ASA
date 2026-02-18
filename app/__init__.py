"""ASA Group — Flask application factory."""

from flask import Flask, render_template

from config import Config


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, template_folder="../templates")
    app.config.from_object(Config)

    # Database
    from app import extensions
    extensions.init_app(app)

    # Initialize tables & seed on first request
    @app.before_request
    def _init_db():
        if not getattr(app, "_db_initialized", False):
            from app.models import init_tables
            from app.seed import seed_all
            init_tables()
            seed_all()
            app._db_initialized = True

    # Register blueprints
    from app.routes.public import public_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app
