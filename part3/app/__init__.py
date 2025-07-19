from flask import Flask
from .config import Config
from .extensions import db, bcrypt, jwt
from .api import init_app as init_api

def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    
    init_api(app)

    return app
