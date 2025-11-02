from flask import request
from flask_restx import Namespace, Resource, fields
from persistence.repository import InMemoryRepository

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True)
})

repo = InMemoryRepository()

@api.route('/')
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        return repo.get_all("amenities")

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
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

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        updates = request.json
        updated = repo.update("amenities", amenity_id, updates)
        if not updated:
            api.abort(404, "Amenity not found")
        return updated
