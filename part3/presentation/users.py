from flask import request
from flask_restx import Namespace, Resource, fields
from business.user import User
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from business.auth_utils import admin_required
from app import db

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

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        users = User.query.all()
        result = []
        for user in users:
            user_data = user.__dict__.copy()
            user_data.pop("_sa_instance_state", None)
            user_data.pop("password", None)
            result.append(user_data)
        return result

    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        data = request.json
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        user_dict = new_user.__dict__.copy()
        user_dict.pop("_sa_instance_state", None)
        user_dict.pop("password", None)
        return user_dict, 201

@api.route('/<string:user_id>')
@api.param('user_id', 'The user ID')
class User(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            api.abort(404, "User not found")
        user_data = user.__dict__.copy()
        user_data.pop("_sa_instance_state", None)
        user_data.pop("password", None)
        return user_data

    @api.expect(user_model)
    @api.marshal_with(user_model)
    @jwt_required()
    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            api.abort(404, "User not found")
        updates = request.json
        if "password" in updates:
            user.password = updates["password"]
        if "first_name" in updates:
            user.first_name = updates["first_name"]
        if "last_name" in updates:
            user.last_name = updates["last_name"]
        if "email" in updates:
            user.email = updates["email"]
        if "is_admin" in updates:
            user.is_admin = updates["is_admin"]
        db.session.commit()
        user_data = user.__dict__.copy()
        user_data.pop("_sa_instance_state", None)
        user_data.pop("password", None)
        return user_data

    @jwt_required()
    @admin_required
    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            api.abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        return '', 204

@api.route('/login')
class UserLogin(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return {"msg": "Invalid email or password"}, 401
        token = create_access_token(identity=user.id)
        return {"access_token": token}, 200

