from flask import request
from flask_restx import Namespace, Resource, fields
from persistence.repository import InMemoryRepository
from business.user import User
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from business.auth_utils import admin_required

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
    @jwt_required()
    def put(self, user_id):
        updates = request.json
        updated_user = repo.update("users", user_id, updates)
        if not updated_user:
            api.abort(404, "User not found")
        updated_user.pop("password", None)
        return updated_user


        @jwt_required()
    @admin_required(repo)
    def delete(self, user_id):
        deleted_user = repo.delete("users", user_id)
        if not deleted_user:
            api.abort(404, "User not found")
        return '', 204

@api.route('/login')
class UserLogin(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")
        users = repo.get_all("users")
        user = next((u for u in users if u.get("email") == email), None)
        if not user:
            return {"msg": "Invalid email or password"}, 401
        user_obj = User(**user)
        if not user_obj.check_password(password):
            return {"msg": "Invalid email or password"}, 401
        token = create_access_token(identity=user["id"])
        return {"access_token": token}, 200
