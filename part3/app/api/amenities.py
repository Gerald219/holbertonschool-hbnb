from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from business.amenity import Amenity
from business.facade import get_repository

amenities_bp = Blueprint('amenities', __name__, url_prefix='/api/v1/amenities')
repo = get_repository(Amenity)

@amenities_bp.route('/', methods=['POST'])
@jwt_required()
def create_amenity():
    identity = get_jwt_identity()
    if not identity.get('is_admin'):
        return jsonify({'message': 'Admin privilege required'}), 403
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({'message': 'Missing name'}), 400
    amenity = Amenity(name=name, description=data.get('description'))
    repo.add(amenity)
    return jsonify(amenity.to_dict()), 201

@amenities_bp.route('/', methods=['GET'])
def list_amenities():
    return jsonify([a.to_dict() for a in repo.list()]), 200

@amenities_bp.route('/<int:amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = repo.get(amenity_id)
    if not amenity:
        return jsonify({'message': 'Amenity not found'}), 404
    return jsonify(amenity.to_dict()), 200

@amenities_bp.route('/<int:amenity_id>', methods=['PUT'])
@jwt_required()
def update_amenity(amenity_id):
    identity = get_jwt_identity()
    if not identity.get('is_admin'):
        return jsonify({'message': 'Admin privilege required'}), 403
    data = request.get_json() or {}
    updates = {}
    if 'name' in data:
        updates['name'] = data['name']
    if 'description' in data:
        updates['description'] = data['description']
    if not updates:
        return jsonify({'message': 'Nothing to update'}), 400
    amenity = repo.update(amenity_id, updates)
    if not amenity:
        return jsonify({'message': 'Amenity not found'}), 404
    return jsonify(amenity.to_dict()), 200

@amenities_bp.route('/<int:amenity_id>', methods=['DELETE'])
@jwt_required()
def delete_amenity(amenity_id):
    identity = get_jwt_identity()
    if not identity.get('is_admin'):
        return jsonify({'message': 'Admin privilege required'}), 403
    amenity = repo.get(amenity_id)
    if not amenity:
        return jsonify({'message': 'Amenity not found'}), 404
    repo.delete(amenity_id)
    return '', 204
