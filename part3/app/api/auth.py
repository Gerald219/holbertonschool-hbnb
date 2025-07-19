from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from business.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Bad credentials'}), 401

    token = create_access_token(identity={'id': user.id, 'is_admin': user.is_admin})
    return jsonify({'access_token': token}), 200
