from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api

db = SQLAlchemy()  # database ORM
migrate = Migrate()  # migrations
bcrypt = Bcrypt()  # password hashing
jwt = JWTManager() # JWT auth tokens
api = Api(title="HBnB API", version="3.0", doc="/docs", prefix="/api/v1") # Swagger at /docs


def init_extensions(app):
    """attach all shared extensions to the Flask app in one place."""
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    api.init_app(app)
