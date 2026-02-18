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

    # App
    APP_NAME = os.environ.get("APP_NAME", "ASA Group")
    APP_PORT = int(os.environ.get("APP_PORT", 5000))
