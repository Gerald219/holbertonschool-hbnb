from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from part3.persistence import sql_repository as repo

api = Namespace("users", description="User operations")

user_model = api.model("User", {
    "id":          fields.String(readonly=True),
    "first_name":  fields.String(required=True),
    "last_name":   fields.String(required=True),
    "email":       fields.String(required=True),
    "password":    fields.String(required=True),
    "created_at":  fields.String(readonly=True),
    "updated_at":  fields.String(readonly=True),
})

user_output = api.model("UserOutput", {
    "id":          fields.String(readonly=True),
    "first_name":  fields.String,
    "last_name":   fields.String,
    "email":       fields.String,
    "created_at":  fields.String(readonly=True),
    "updated_at":  fields.String(readonly=True),
})

user_update = api.model("UserUpdate", {
    "first_name":  fields.String,
    "last_name":   fields.String,
    "email":       fields.String,
})

@api.route("/")
class UserList(Resource):
    @api.marshal_list_with(user_output, code=200)
    def get(self):
        return repo.list_users()

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_output, code=201)
    def post(self):
        data = request.get_json(force=True) or {}
        try:
            return repo.create_user(data), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route("/<string:user_id>")
@api.param("user_id", "The user ID")
class UserItem(Resource):
    @api.marshal_with(user_output, code=200)
    def get(self, user_id):
        u = repo.get_user(user_id)
        if not u:
            api.abort(404, "User not found")
        return u

    @jwt_required()
    @api.expect(user_update, validate=True)
    @api.marshal_with(user_output, code=200)
    def put(self, user_id):
        current_user = get_jwt_identity()
        is_admin = bool(get_jwt().get("is_admin", False))
        if (current_user != user_id) and (not is_admin):
            api.abort(403, "You can only update your own profile (or be an admin).")
        updates = request.get_json(force=True) or {}
        for k in ("id", "password", "password_hash", "is_admin", "created_at", "updated_at"):
            updates.pop(k, None)
        try:
            updated = repo.update_user(user_id, updates)
        except ValueError as e:
            api.abort(400, str(e))
        if not updated:
            api.abort(404, "User not found")
        return updated

    @jwt_required()
    @api.response(204, "Deleted")
    def delete(self, user_id):
        current_user = get_jwt_identity()
        is_admin = bool(get_jwt().get("is_admin", False))
        if (current_user != user_id) and (not is_admin):
            api.abort(403, "You can only delete your own account (or be an admin).")
        if not repo.delete_user(user_id):
            api.abort(404, "User not found")
        return "", 204
