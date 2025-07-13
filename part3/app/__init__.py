from flask_jwt_extended import JWTManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    jwt = JWTManager(app)
    db.init_app(app)
    return app
