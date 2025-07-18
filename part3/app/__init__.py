from flask import Flask
from .config import Config
from .extensions import db, bcrypt, jwt

def create_app(config_object=Config):
    """Application factory to set up Flask app and extensions."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    return app
