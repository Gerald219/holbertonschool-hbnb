from flask import request
from flask_restx import Namespace, Resource, fields
from part3.persistence.user_storage import repo
from flask_jwt_extended import jwt_required, get_jwt


api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True)
})


@api.route('/')
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        return repo.get_all("amenities")

    @jwt_required()
    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        claims = get_jwt()
        if not bool(claims.get("is_admin", False)):
            api.abort(403, "Admin only: you must be an admin to create amenities")

        data = request.json
        return repo.save("amenities", data), 201

@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity ID')
class Amenity(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        amenity = repo.get("amenities", amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        claims = get_jwt()
        if not bool(claims.get("is_admin", False)):
            api.abort(403, "Admin only: you must be an admin to update amenities")

        updates = request.json or {}
        updated = repo.update("amenities", amenity_id, updates)
        if not updated:
            api.abort(404, "Amenity not found")
        return updated
