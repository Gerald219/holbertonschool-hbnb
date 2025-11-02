from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api

db = SQLAlchemy()  # database ORM
migrate = Migrate()  # migrations
bcrypt = Bcrypt()  # password hashing
jwt = JWTManager() # JWT auth tokens
api = Api(title="HBnB API", version="3.0", doc="/docs")  # Swagger at /docs
