from flask import Flask
from part3.config import DevConfig  # Importing DevConfig

def create_app(config_object=DevConfig):
    """
    This function makes your Flask app.
    it is a config (settings), loads routes.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)  # Load config settings

    @app.route("/")
    def root():
        return "HBnB API part 3 is running! ON AIR!"

    return app
