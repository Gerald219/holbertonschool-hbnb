from flask import Flask
from flask_restx import Api
from presentation.users import api as users_namespace
from presentation.places import api as places_namespace
from presentation.amenities import api as amenities_namespace
from presentation.reviews import api as reviews_namespace  # ✅ New

app = Flask(__name__)
api = Api(app, doc='/docs')

# Register all namespaces
api.add_namespace(users_namespace, path="/api/v1/users")
api.add_namespace(places_namespace, path="/api/v1/places")
api.add_namespace(amenities_namespace, path="/api/v1/amenities")
api.add_namespace(reviews_namespace, path="/api/v1/reviews")  # ✅ New

@app.route('/')
def home():
    return "HBnB API is running!"

if __name__ == "__main__":
    app.run(debug=True)
