from flask import request
from flask_restx import Namespace, Resource, fields
from persistence.repository import InMemoryRepository

api = Namespace('users', description='User operations')

# Original combined model stays as the CREATE (input) schema
user_model = api.model('User', {
    'id': fields.String(readonly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True)
})

# NEW: output schema (no password) and update schema (all optional)
user_output = api.model('UserOutput', {
    'id':         fields.String(readonly=True),
    'first_name': fields.String,
    'last_name':  fields.String,
    'email':      fields.String,
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True),
})

user_update = api.model('UserUpdate', {
    'first_name': fields.String(required=False),
    'last_name':  fields.String(required=False),
    'email':      fields.String(required=False),
    'password':   fields.String(required=False),
})

repo = InMemoryRepository()

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_output, code=200)  # hide password in list
    def get(self):
        return repo.get_all("users")

    @api.expect(user_model, validate=True)         # require password on create
    @api.marshal_with(user_output, code=201)       # do not return password
    def post(self):
        data = request.json or {}
        created = repo.save("users", data)
        return created, 201

@api.route('/<string:user_id>')
@api.param('user_id', 'The user ID')
class User(Resource):
    @api.marshal_with(user_output, code=200)       # hide password on single GET
    def get(self, user_id):
        user = repo.get("users", user_id)
        if not user:
            api.abort(404, "User not found")
        return user

    @api.expect(user_update, validate=True)        # allow partial updates
    @api.marshal_with(user_output, code=200)       # never return password
    def put(self, user_id):
        updates = request.json or {}
        updated_user = repo.update("users", user_id, updates)
        if not updated_user:
            api.abort(404, "User not found")
        return updated_user

    # Part 2 spec: DELETE for users is not implemented
    def delete(self, user_id):
        api.abort(405, "DELETE not supported for users in Part 2")
