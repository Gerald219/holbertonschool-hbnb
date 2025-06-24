from flask import request
from flask_restx import Namespace, Resource, fields
from persistence.repository import InMemoryRepository

api = Namespace('reviews', description='Review operations')
repo = InMemoryRepository()

review_model = api.model('Review', {
    'id': fields.String(readonly=True),
    'text': fields.String(required=True),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True)
})

@api.route('/')
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        return repo.get_all("reviews")

    @api.expect(review_model)
    @api.marshal_with(review_model, code=201)
    def post(self):
        data = request.json
        return repo.save("reviews", data), 201

@api.route('/<string:review_id>')
@api.param('review_id', 'The review ID')
class Review(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id):
        review = repo.get("reviews", review_id)
        if not review:
            api.abort(404, "Review not found")
        return review

    @api.expect(review_model)
    @api.marshal_with(review_model)
    def put(self, review_id):
        updates = request.json
        updated = repo.update("reviews", review_id, updates)
        if not updated:
            api.abort(404, "Review not found")
        return updated

    def delete(self, review_id):
        deleted = repo.delete("reviews", review_id)
        if not deleted:
            api.abort(404, "Review not found")
        return '', 204
