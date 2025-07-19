from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from business.user import User
from business.facade import get_repository

users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')
repo = get_repository(User)

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    for field in ('first_name', 'last_name', 'email', 'password'):
        if field not in data:
            return jsonify({'message': f'Missing {field}'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already in use'}), 400

    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email']
    )
    user.set_password(data['password'])
    repo.add(user)
    return jsonify(user.to_dict()), 201

