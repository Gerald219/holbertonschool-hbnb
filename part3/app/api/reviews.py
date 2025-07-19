from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from business.review import Review
from business.place import Place
from business.facade import get_repository

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api/v1')
repo = get_repository(Review)

    @reviews_bp.route('/places/<int:place_id>/reviews', methods=['POST'])
@jwt_required()
def create_review(place_id):
    data = request.get_json() or {}
    for field in ('text', 'rating'):
        if field not in data:
            return jsonify({'message': f'Missing {field}'}), 400

    place = get_repository(Place).get(place_id)
    if not place:
        return jsonify({'message': 'Place not found'}), 404
    
        identity = get_jwt_identity()
    review = Review(
        user_id=identity['id'],
        place_id=place_id,
        text=data['text'],
        rating=data['rating']
    )
    repo.add(review)
    return jsonify(review.to_dict()), 201

    @reviews_bp.route('/places/<int:place_id>/reviews', methods=['GET'])
def list_reviews(place_id):
    reviews = repo.list()
    place_reviews = [r.to_dict() for r in reviews if r.place_id == place_id]
    return jsonify(place_reviews), 200

    @reviews_bp.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = repo.get(review_id)
    if not review:
        return jsonify({'message': 'Review not found'}), 404
    return jsonify(review.to_dict()), 200

