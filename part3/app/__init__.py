from flask_jwt_extended import JWTManager
from flask import Flask

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    jwt = JWTManager(app)
    return app
