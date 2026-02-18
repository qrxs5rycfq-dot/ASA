"""Entry point for the ASA Group application."""

from app import create_app
from config import Config

application = create_app()

if __name__ == "__main__":
    application.run(debug=False, host="0.0.0.0", port=Config.APP_PORT)
