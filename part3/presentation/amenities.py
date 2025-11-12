from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from part3.persistence import sql_amenity_repository as repo

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
        return repo.list_amenities()

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        claims = get_jwt()
        if not bool(claims.get("is_admin", False)):
            api.abort(403, "Admin only: you must be an admin to create amenities")
        data = request.get_json(force=True) or {}
        name = (data.get("name") or "").strip()
        if not name:
            api.abort(400, "name is required")
        return repo.create_amenity({"name": name}), 201

@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity ID')
class Amenity(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        amenity = repo.get_amenity(amenity_id)
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
        updates = request.get_json(force=True) or {}
        updated = repo.update_amenity(amenity_id, updates)
        if not updated:
            api.abort(404, "Amenity not found")
        return updated

    @jwt_required()
    @api.response(204, 'Deleted')
    def delete(self, amenity_id):
        claims = get_jwt()
        if not bool(claims.get("is_admin", False)):
            api.abort(403, "Admin only: you must be an admin to delete amenities")
        deleted = repo.delete_amenity(amenity_id)
        if not deleted:
            api.abort(404, "Amenity not found")
        return '', 204
