from flask import Flask
from part3.config import DevConfig  # Importing DevConfig
from part3.app.extensions import db, migrate, bcrypt, jwt, api
from part3.presentation.users import api as users_ns
from part3.presentation.places import api as places_ns
from part3.presentation.amenities import api as amenities_ns
from part3.presentation.reviews import api as reviews_ns


def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)  # Load config settings

    # plug in tools
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    # register existing namespaces from Part 2
    api.add_namespace(users_ns, path="/users")
    api.add_namespace(places_ns, path="/places")
    api.add_namespace(amenities_ns, path="/amenities")
    api.add_namespace(reviews_ns, path="/reviews")

    @app.route("/", endpoint="healthcheck")
    def home():
        return "HBnB API part 3 is running! ON AIR!"

    return app
