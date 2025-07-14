from flask import request
from flask_restx import Namespace, Resource, fields
from business.place import Place
from app import db
from flask_jwt_extended import jwt_required
from business.auth_utils import admin_required

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
        places = Place.query.all()
        result = []
        for place in places:
            place_data = place.__dict__.copy()
            place_data.pop("_sa_instance_state", None)
            result.append(place_data)
        return result

    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)
    def post(self):
        data = request.json
        new_place = Place(**data)
        db.session.add(new_place)
        db.session.commit()
        place_dict = new_place.__dict__.copy()
        place_dict.pop("_sa_instance_state", None)
        return place_dict, 201

@api.route('/<string:place_id>')
@api.param('place_id', 'The place ID')
class Place(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id):
        place = Place.query.get(place_id)
        if not place:
            api.abort(404, "Place not found")
        place_data = place.__dict__.copy()
        place_data.pop("_sa_instance_state", None)
        return place_data

    @api.expect(place_model)
    @api.marshal_with(place_model)
    def put(self, place_id):
        place = Place.query.get(place_id)
        if not place:
            api.abort(404, "Place not found")
        updates = request.json
        for key, value in updates.items():
            setattr(place, key, value)
        db.session.commit()
        updated_place = place.__dict__.copy()
        updated_place.pop("_sa_instance_state", None)
        return updated_place

    @jwt_required()
    @admin_required
    def delete(self, place_id):
        place = Place.query.get(place_id)
        if not place:
            api.abort(404, "Place not found")
        db.session.delete(place)
        db.session.commit()
        return '', 204
