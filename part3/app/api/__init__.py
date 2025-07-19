from .auth import auth_bp
from .users import users_bp
from .places import places_bp
from .reviews import reviews_bp
from .amenities import amenities_bp

def init_app(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(amenities_bp)
