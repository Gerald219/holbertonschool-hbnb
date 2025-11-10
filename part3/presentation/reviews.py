from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from part3.persistence.user_storage import repo

api = Namespace("reviews", description="Review operations")

# Client input for create
review_input = api.model("ReviewInput", {
    "text": fields.String(required=True),
    "place_id": fields.String(required=True),
})

# Server output shape
review_output = api.model("ReviewOutput", {
    "id": fields.String(readonly=True),
    "text": fields.String,
    "user_id": fields.String,   # set from JWT
    "place_id": fields.String,
    "created_at": fields.String(readonly=True),
    "updated_at": fields.String(readonly=True),
})

# Partial update (author can edit text only)
review_update = api.model("ReviewUpdate", {
    "text": fields.String(required=True),
})

@api.route("/")
class ReviewList(Resource):
    @api.marshal_list_with(review_output)
    def get(self):
        return repo.get_all("reviews")

    @jwt_required()
    @api.expect(review_input, validate=True)
    @api.marshal_with(review_output, code=201)
    def post(self):
        data = request.get_json(force=True) or {}
        user_id = get_jwt_identity()
        place_id = data["place_id"]

        # place must exist
        place = repo.get("places", place_id)
        if not place:
            api.abort(404, "Place not found")

        # no self-review
        if place.get("owner_id") == user_id:
            api.abort(403, "You cannot review your own place")

        # one review per user per place
        for r in repo.get_all("reviews"):
            if r.get("user_id") == user_id and r.get("place_id") == place_id:
                api.abort(409, "You already reviewed this place")

        review = {"text": data["text"], "place_id": place_id, "user_id": user_id}
        created = repo.save("reviews", review)
        return created, 201

@api.route("/<string:review_id>")
@api.param("review_id", "The review ID")
class Review(Resource):
    @api.marshal_with(review_output)
    def get(self, review_id):
        review = repo.get("reviews", review_id)
        if not review:
            api.abort(404, "Review not found")
        return review

    @jwt_required()
    @api.expect(review_update, validate=True)
    @api.marshal_with(review_output, code=200)
    def put(self, review_id):
        review = repo.get("reviews", review_id)
        if not review:
            api.abort(404, "Review not found")

        # AUTHOR-ONLY edit (admins cannot edit)
        current_user = get_jwt_identity()
        if review.get("user_id") != current_user:
            api.abort(403, "Only the author can edit this review")

        text = request.get_json(force=True).get("text")
        if text is None:
            api.abort(400, "Nothing to update")

        updated = repo.update("reviews", review_id, {"text": text})
        return updated, 200

    @jwt_required()
    @api.response(204, "Deleted")
    def delete(self, review_id):
        review = repo.get("reviews", review_id)
        if not review:
            api.abort(404, "Review not found")

        # Author OR admin can delete
        current_user = get_jwt_identity()
        is_admin = bool(get_jwt().get("is_admin", False))
        if not (is_admin or review.get("user_id") == current_user):
            api.abort(403, "Only the author or an admin can delete this review")

        deleted = repo.delete("reviews", review_id)
        if not deleted:
            api.abort(404, "Review not found")
        return "", 204

