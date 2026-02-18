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

    # Context processor to inject site settings into all templates
    @app.context_processor
    def inject_site_settings():
        try:
            from app.extensions import get_db
            db = get_db()
            cur = db.cursor()
            cur.execute("SELECT setting_key, setting_value FROM site_settings")
            rows = cur.fetchall()
            cur.close()
            settings = {r["setting_key"]: r["setting_value"] for r in rows}
            return {"site": settings}
        except Exception:
            return {"site": {"app_name": "ASA Group", "logo_url": "", "tagline": "General Supplier & Kontraktor"}}

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
