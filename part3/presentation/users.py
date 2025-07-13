from flask import request
from flask_restx import Namespace, Resource, fields
from persistence.repository import InMemoryRepository
from business.user import User

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.String(readonly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True)
})

repo = InMemoryRepository()

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        users = repo.get_all("users")
        for user in users:
        user.pop("password", None)
        return users

    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        data = request.json
        new_user = User(**data)
        user_dict = new_user.__dict__.copy()
        user_dict.pop("password", None)
        repo.save("users", user_dict)
        return user_dict, 201

@api.route('/<string:user_id>')
@api.param('user_id', 'The user ID')
class User(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        user = repo.get("users", user_id)
        if not user:
            api.abort(404, "User not found")
        user.pop("password", None)
        return user

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        updates = request.json
        updated_user = repo.update("users", user_id, updates)
        if not updated_user:
            api.abort(404, "User not found")
        updated_user.pop("password", None)
        return updated_user

    def delete(self, user_id):
        deleted_user = repo.delete("users", user_id)
        if not deleted_user:
            api.abort(404, "User not found")
        return '', 204
