from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from business.user import User
from business.facade import get_repository

users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')
repo = get_repository(User)

