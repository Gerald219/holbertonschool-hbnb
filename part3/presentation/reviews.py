from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from part3.persistence.user_storage import repo

api = Namespace('reviews', description='Review operations')

# Input from client (only allowed fields)
review_input = api.model('ReviewInput', {
    'text': fields.String(required=True),
    'place_id': fields.String(required=True),
})

# Output shape returned to clients
review_output = api.model('ReviewOutput', {
    'id': fields.String(readonly=True),
    'text': fields.String,
    'user_id': fields.String,      # set by server from JWT
    'place_id': fields.String,
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True),
})

# Partial update (author can edit text)
review_update = api.model('ReviewUpdate', {
    'text': fields.String(required=True),
})

@api.route('/')
class ReviewList(Resource):
    @api.marshal_list_with(review_output)
    def get(self):
        return repo.get_all("reviews")

    @jwt_required()
    @api.expect(review_input, validate=True)
    @api.marshal_with(review_output, code=201)
    def post(self):
        data = request.json or {}
        current_user = get_jwt_identity()

        # validate place exists
        place_id = data.get("place_id")
        place = repo.get("places", place_id)
        if not place:
            api.abort(404, "Place not found")

        # no self-review(owner cannot review own place)
        if place.get("owner_id") == current_user:
            api.abort(403, "You cannot review your own place")

        # one review per user per place
        for r in repo.get_all("reviews"):
            if r.get("user_id") == current_user and r.get("place_id") == place_id:
                api.abort(409, "You already reviewed this place")

        # create review(server sets user_id)
        review = {
            "text": data["text"],
            "place_id": place_id,
            "user_id": current_user,
        }
        saved = repo.save("reviews", review)
        return saved, 201

@api.route('/<string:review_id>')
@api.param('review_id', 'The review ID')
class Review(Resource):
    @api.marshal_with(review_output)
    def get(self, review_id):
        review = repo.get("reviews", review_id)
        if not review:
            api.abort(404, "Review not found")
        return review

    @jwt_required()
    @api.expect(review_update, validate=True)
    @api.marshal_with(review_output)
    def put(self, review_id):
        current_user = get_jwt_identity()
        existing = repo.get("reviews", review_id)
        if not existing:
            api.abort(404, "Review not found")

        # only author can edit
        if existing.get("user_id") != current_user:
            api.abort(403, "You can only edit your own review")

        updates = request.json or {}
        # restrict to text only
        allowed = {"text"}
        filtered = {k: v for k, v in updates.items() if k in allowed}
        if "text" not in filtered:
            api.abort(400, "Nothing to update")

        updated = repo.update("reviews", review_id, filtered)
        if not updated:
            api.abort(404, "Review not found")
        return updated

    @jwt_required()
    @api.response(204, 'Deleted')
    def delete(self, review_id):
        current_user = get_jwt_identity()
        existing = repo.get("reviews", review_id)
        if not existing:
            api.abort(404, "Review not found")

        if existing.get("user_id") != current_user:
            api.abort(403, "You can only delete your own review")

        deleted = repo.delete("reviews", review_id)
        if not deleted:
            api.abort(404, "Review not found")
        return '', 204
