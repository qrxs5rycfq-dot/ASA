import os
import secrets

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(32))
    FLASK_ENV = os.environ.get("FLASK_ENV", "production")

    # MySQL
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = int(os.environ.get("DB_PORT", 3306))
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_NAME = os.environ.get("DB_NAME", "asa_group")
    DB_UNIX_SOCKET = os.environ.get("DB_UNIX_SOCKET", "")

    # App
    APP_NAME = os.environ.get("APP_NAME", "ASA Group")
    APP_PORT = int(os.environ.get("APP_PORT", 5000))

    # Upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "uploads")
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_UPLOAD_MB", 5)) * 1024 * 1024
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "svg"}
