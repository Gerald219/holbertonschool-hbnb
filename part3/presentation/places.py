from flask import request
from flask_restx import Namespace, Resource, fields
from part3.persistence.user_storage import repo
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')


place_model = api.model('Place', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True),
    'description': fields.String(),
    'city': fields.String(),
    'price_per_night': fields.Integer(),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
    'owner_id': fields.String(required=True),
    'amenity_ids': fields.List(fields.String),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True)
})

@api.route('/')
class PlaceList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        return repo.get_all("places")

    @jwt_required()  # Require a valid JWT to access this endpoint
    @api.expect(place_model, validate=True)
    @api.marshal_with(place_model, code=201)
    def post(self):
        data = request.get_json(force=True) or {}
        data["user_id"] = get_jwt_identity()  # tag owner from the JWT
        created = repo.save("places", data)
        return created, 201


@api.route('/<string:place_id>')
@api.param('place_id', 'The place ID')
class Place(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id):
        place = repo.get("places", place_id)
        if not place:
            api.abort(404, "Place not found")
        return place

    @api.expect(place_model)
    @api.marshal_with(place_model)
    def put(self, place_id):
        updates = request.json
        updated = repo.update("places", place_id, updates)
        if not updated:
            api.abort(404, "Place not found")
        return updated
