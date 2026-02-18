import pymysql
from flask import g, current_app


def get_db():
    """Get a MySQL database connection for the current request."""
    if "db" not in g:
        kwargs = dict(
            host=current_app.config["DB_HOST"],
            port=current_app.config["DB_PORT"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
            database=current_app.config["DB_NAME"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
            charset="utf8mb4",
        )
        unix_socket = current_app.config.get("DB_UNIX_SOCKET")
        if unix_socket:
            kwargs["unix_socket"] = unix_socket
            kwargs.pop("host", None)
            kwargs.pop("port", None)
        g.db = pymysql.connect(**kwargs)
    return g.db


def close_db(exc=None):
    """Close the database connection at the end of the request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    """Register database teardown with the Flask app."""
    app.teardown_appcontext(close_db)
