from __future__ import annotations
from typing import Dict, Any
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from part3.persistence import sql_repository as repo

api = Namespace("users", description="User operations")


user_input = api.model("UserInput", {
    "first_name":  fields.String(required=True),
    "last_name":   fields.String(required=True),
    "email":       fields.String(required=True),
    "password":    fields.String(required=True),
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
    "first_name":  fields.String(required=False),
    "last_name":   fields.String(required=False),
    "email":       fields.String(required=False),
})


@api.route("/")
class UserList(Resource):
    @api.marshal_list_with(user_output, code=200)
    def get(self):
        return repo.list_users()

    @api.expect(user_input, validate=True)
    @api.marshal_with(user_output, code=201)
    def post(self):
        payload: Dict[str, Any] = request.get_json(force=True) or {}
        try:
            created = repo.create_user(payload)
            return created, 201
        except ValueError as e:

            return {"message": str(e)}, 400


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
        # Guard rails: block dangerous fields
        for k in ("id", "password", "password_hash", "created_at", "updated_at", "is_admin"):
            updates.pop(k, None)

        try:
            updated = repo.update_user(user_id, updates)
        except ValueError as e:
            return {"message": str(e)}, 400
        if not updated:
            api.abort(404, "User not found")
        return updated, 200

    @jwt_required()
    @api.response(204, "Deleted")
    def delete(self, user_id):
        current_user = get_jwt_identity()
        is_admin = bool(get_jwt().get("is_admin", False))
        if (current_user != user_id) and (not is_admin):
            api.abort(403, "You can only delete your own account (or be an admin).")

        ok = repo.delete_user(user_id)
        if not ok:
            api.abort(404, "User not found")
        return "", 204
