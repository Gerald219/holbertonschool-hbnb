from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from part3.persistence import sql_place_repository as repo  # <-- DB repo

api = Namespace("places", description="Place operations")

place_input = api.model("PlaceInput", {
    "name": fields.String(required=True),
    "city": fields.String(required=True),
    "price_per_night": fields.Integer(required=True),
    "description": fields.String,
    "latitude": fields.Float,
    "longitude": fields.Float,
})

place_output = api.model("PlaceOutput", {
    "id": fields.String(readonly=True),
    "name": fields.String,
    "description": fields.String,
    "city": fields.String,
    "price_per_night": fields.Integer,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "owner_id": fields.String,
    "amenity_ids": fields.List(fields.String),
    "created_at": fields.String(readonly=True),
    "updated_at": fields.String(readonly=True),
})

place_update = api.model("PlaceUpdate", {
    "name": fields.String,
    "city": fields.String,
    "price_per_night": fields.Integer,
    "description": fields.String,
    "latitude": fields.Float,
    "longitude": fields.Float,
})

@api.route("/")
class PlaceList(Resource):
    @api.marshal_list_with(place_output)
    def get(self):
        return repo.list_places()

    @jwt_required()
    @api.expect(place_input, validate=True)
    @api.marshal_with(place_output, code=201)
    def post(self):
        data = request.get_json(force=True) or {}

        # Validate price_per_night, latitude, and longitude
        if not data.get("price_per_night") or not isinstance(data["price_per_night"], int) or data["price_per_night"] <= 0:
            api.abort(400, "invalid_value: price_per_night")
    
        if "latitude" in data and not isinstance(data["latitude"], (float, int)):
            api.abort(400, "invalid_value: latitude")
    
        if "longitude" in data and not isinstance(data["longitude"], (float, int)):
            api.abort(400, "invalid_value: longitude")
    
        data["owner_id"] = get_jwt_identity()
        created = repo.create_place(data)
        return created, 201


@api.route("/<string:place_id>")
@api.param("place_id", "The place ID")
class Place(Resource):
    @api.marshal_with(place_output)
    def get(self, place_id):
        place = repo.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return place

    @jwt_required()
    @api.expect(place_update, validate=True)
    @api.marshal_with(place_output, code=200)
    def put(self, place_id):
    current_user = get_jwt_identity()
    is_admin = bool(get_jwt().get("is_admin", False))

        existing = repo.get_place(place_id)
        if not existing:
            api.abort(404, "Place not found")

        # Admin or owner check
        if not is_admin and existing.get("owner_id") != current_user:
            api.abort(403, "Only the owner (or admin) can update this place")

        updates = request.get_json(force=True) or {}
        updated = repo.update_place(place_id, updates)
        return updated, 200


    @jwt_required()
    @api.response(204, "Deleted")
    def delete(self, place_id):
        current_user = get_jwt_identity()
        is_admin = bool(get_jwt().get("is_admin", False))

        # Check if the place exists
        existing = repo.get_place(place_id)
        if not existing:
            api.abort(404, "Place not found")

        # Check if user is owner or admin
        if existing.get("owner_id") != current_user and not is_admin:
            api.abort(403, "Only the owner or an admin can delete this place")

        # Delete the place
        deleted = repo.delete_place(place_id)
        if not deleted:
            api.abort(404, "Place not found")

        return "", 204


@api.route("/<string:place_id>/amenities/<string:amenity_id>")
@api.param("place_id", "The place ID")
@api.param("amenity_id", "The amenity ID")
class PlaceAmenity(Resource):
    @jwt_required()
    @api.marshal_with(place_output, code=200)
    def post(self, place_id, amenity_id):
        current_user = get_jwt_identity()
        is_admin = bool(get_jwt().get("is_admin", False))

        existing = repo.get_place(place_id)
        if not existing:
            api.abort(404, "Place not found")

        if (existing.get("owner_id") != current_user) and (not is_admin):
            api.abort(403, "Only the owner or an admin can modify amenities for this place")

        updated = repo.attach_amenity(place_id, amenity_id)
        if not updated:
            api.abort(404, "Amenity or place not found")
        return updated, 200

    @jwt_required()
    @api.marshal_with(place_output, code=200)
    def delete(self, place_id, amenity_id):
        current_user = get_jwt_identity()
        is_admin = bool(get_jwt().get("is_admin", False))

        existing = repo.get_place(place_id)
        if not existing:
            api.abort(404, "Place not found")

        if (existing.get("owner_id") != current_user) and (not is_admin):
            api.abort(403, "Only the owner or an admin can change amenities for this place")

        updated = repo.detach_amenity(place_id, amenity_id)
        if not updated:
            api.abort(404, "Amenity or place not found")
        return updated, 200

