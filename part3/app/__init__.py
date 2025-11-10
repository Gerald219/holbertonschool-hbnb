from flask import Flask
from part3.config import DevConfig  # Importing DevConfig
from part3.app.extensions import db, migrate, bcrypt, jwt, api
from part3.presentation.users import api as users_ns
from part3.presentation.places import api as places_ns
from part3.presentation.amenities import api as amenities_ns
from part3.presentation.reviews import api as reviews_ns
from part3.presentation.auth import api as auth_ns
from flask import jsonify
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import InvalidTokenError
from part3.app.extensions import init_extensions


def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)  # Load config settings

    
    init_extensions(app)  # Initialize extensions with the app -Yay!

    @jwt.unauthorized_loader
    def _jwt_unauthorized(reason):
        return jsonify(message="Missing or invalid Authorization header"), 401

    @jwt.invalid_token_loader
    def _jwt_invalid(reason):
        return jsonify(message="Invalid token"), 422

    @jwt.expired_token_loader
    def _jwt_expired(jwt_header, jwt_payload):
        return jsonify(message="Token has expired"), 401

    @app.errorhandler(NoAuthorizationError)
    def _no_auth_header(e):
        return jsonify(message="Missing Authorization header"), 401
    
    @api.errorhandler(NoAuthorizationError)
    def _restx_no_auth(e):
        return {"message": "Missing or invalid Authorization header"}, 401
    
    @api.errorhandler(JWTExtendedException)
    def _restx_jwt_errors(e):
        return {"message": "Invalid token"}, 422
    
    @app.errorhandler(JWTExtendedException)
    def _jwt_all(e):
        return jsonify(message="Invalid token"), 422

    @api.errorhandler(InvalidTokenError)
    def _restx_invalid_token(e):
        return {"message": "Invalid token"}, 422

    @app.errorhandler(InvalidTokenError)
    def _app_invalid_token(e):
        return jsonify(message="Invalid token"), 422


    # register existing namespaces from Part2
    api.add_namespace(users_ns, path="/users")
    api.add_namespace(places_ns, path="/places")
    api.add_namespace(amenities_ns, path="/amenities")
    api.add_namespace(reviews_ns, path="/reviews")
    api.add_namespace(auth_ns, path="/auth")

    @app.route("/", endpoint="healthcheck")
    def home():
        return "HBnB API part 3 is running! ON AIR!"

    return app
