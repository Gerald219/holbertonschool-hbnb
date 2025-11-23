from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from part3.persistence import sql_review_repository as repo

api = Namespace("reviews", description="Review operations")

review_input = api.model("ReviewInput", {
    "text": fields.String(required=True),
    "place_id": fields.String(required=True),
})

review_output = api.model("ReviewOutput", {
    "id": fields.String(readonly=True),
    "text": fields.String,
    "user_id": fields.String,
    "place_id": fields.String,
    "created_at": fields.String(readonly=True),
    "updated_at": fields.String(readonly=True),
})

review_update = api.model("ReviewUpdate", {
    "text": fields.String(required=True),
})


@api.route("/")
class ReviewList(Resource):
    @api.marshal_list_with(review_output)
    def get(self):
        ## list all reviews
        return repo.list_reviews()

    @jwt_required()
    @api.expect(review_input, validate=True)
    @api.marshal_with(review_output, code=201)
    def post(self):
        ## create a new review for a place (user comes from JWT)
        data = request.get_json(force=True) or {}
        user_id = get_jwt_identity()

        payload = {
            "text": data.get("text"),
            "place_id": data.get("place_id"),
            "user_id": user_id,
        }

        try:
            created = repo.create_review(payload)
        except ValueError as e:
            msg = str(e)
            if msg == "missing_required_fields":
                api.abort(400, "missing_required_fields")
            if msg == "place_not_found":
                api.abort(404, "Place not found")
            if msg == "self_review_forbidden":
                api.abort(403, "You cannot review your own place")
            if msg == "duplicate_review":
                api.abort(409, "You already reviewed this place")
            api.abort(400, msg)

        return created, 201


@api.route("/<string:review_id>")
@api.param("review_id", "The review ID")
class Review(Resource):
    @api.marshal_with(review_output)
    def get(self, review_id):
        ## fetch single review
        r = repo.get_review(review_id)
        if not r:
            api.abort(404, "Review not found")
        return r

    @jwt_required()
    @api.expect(review_update, validate=True)
    @api.marshal_with(review_output, code=200)
    def put(self, review_id):
        ## author-only edit
        updates = request.get_json(force=True) or {}
        try:
            updated = repo.update_review(review_id, updates, actor_id=get_jwt_identity())
        except ValueError as e:
            m = str(e)
            if m == "forbidden_not_author":
                api.abort(403, "Only the author can edit this review")
            if m == "nothing_to_update":
                api.abort(400, "Nothing to update")
            api.abort(400, m)
        if not updated:
            api.abort(404, "Review not found")
        return updated, 200

    @jwt_required()
    @api.response(204, "Deleted")
    def delete(self, review_id):
        ## author OR admin delete
        claims = get_jwt()
        is_admin = bool(claims.get("is_admin", False))
        try:
            ok = repo.delete_review(
                review_id,
                actor_id=get_jwt_identity(),
                is_admin=is_admin,
            )
        except ValueError as e:
            if str(e) == "forbidden_delete":
                api.abort(403, "Only the author or an admin can delete this review")
            api.abort(400, str(e))
        if not ok:
            api.abort(404, "Review not found")
        return "", 204

