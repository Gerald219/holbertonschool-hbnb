from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from business.review import Review
from business.place import Place
from business.facade import get_repository

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api/v1')
repo = get_repository(Review)

