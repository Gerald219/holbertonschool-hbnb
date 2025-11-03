from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from part3.persistence.user_storage import repo
from flask_restx import fields

api = Namespace("places", description="Place operations")

# Input schema: what client sends
place_input = api.model("PlaceInput", {
    "name": fields.String(required=True),
    "city": fields.String(required=True),
    "price_per_night": fields.Integer(required=True),
    "description": fields.String,
    "latitude": fields.Float,
    "longitude": fields.Float,
})

# Output schema: what server returns
place_output = api.model("PlaceOutput", {
    "id": fields.String(readonly=True),
    "name": fields.String,
    "description": fields.String,
    "city": fields.String,
    "price_per_night": fields.Integer,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "owner_id": fields.String,  # set by server from JWT
    "amenity_ids": fields.List(fields.String),
    "created_at": fields.String(readonly=True),
    "updated_at": fields.String(readonly=True),
})

place_update = api.model('PlaceUpdate', {
    'name': fields.String,
    'city': fields.String,
    'price_per_night': fields.Integer,
    'description': fields.String,
    'latitude': fields.Float,
    'longitude': fields.Float,
})

@api.route("/")
class PlaceList(Resource):
    @api.marshal_list_with(place_output)
    def get(self):
        return repo.get_all("places")

    @jwt_required()
    @api.expect(place_input, validate=True)        # client does NOT send owner_id
    @api.marshal_with(place_output, code=201)      # server returns owner_id
    def post(self):
        data = request.get_json(force=True) or {}
        data["owner_id"] = get_jwt_identity()      # stamp owner from JWT
        created = repo.save("places", data)
        return created, 201

@api.route("/<string:place_id>")
@api.param("place_id", "The place ID")
class Place(Resource):
    @api.marshal_with(place_output)
    def get(self, place_id):
        place = repo.get("places", place_id)
        if not place:
            api.abort(404, "Place not found")
        return place

    @jwt_required()
    @api.expect(place_update, validate=True)
    @api.marshal_with(place_output, code=200)
    def put(self, place_id):
        place = repo.get("places", place_id)
        if not place:
            api.abort(404, "Place not found")

        current_user = get_jwt_identity()
        if place.get("owner_id") != current_user:
            api.abort(403, "You can only edit your own place")

        updates = request.get_json(force=True) or {}
        updates.pop("owner_id", None)  # prevent ownership change
        updated = repo.update("places", place_id, updates)
        return updated, 200
