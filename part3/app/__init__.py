from flask import Flask

def create_app(config_object=None):
    """
    This function makes your Flask app.
    it is a config (settings), loads routes.
    """
    app = Flask(__name__)
    if config_object is not None:
        app.config.from_object(config_object)

    @app.route("/")
    def root():
        return "HBnB API part 3 is running! ON AIR!"

    return app
