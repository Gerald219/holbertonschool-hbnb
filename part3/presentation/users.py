from __future__ import annotations
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from business.facade import Facade  # Import Facade class

api = Namespace("users", description="User operations")

# Instantiate the Facade
facade = Facade()

user_input = api.model("UserInput", {
    "first_name":  fields.String(required=True),
    "last_name":   fields.String(required=True),
    "email":       fields.String(required=True),
    "password":    fields.String(required=True),
})

user_update = api.model("UserUpdate", {
    "first_name":  fields.String(),
    "last_name":   fields.String(),
    "email":       fields.String(),
})

user_output = api.model("UserOutput", {
    "id":          fields.String(readonly=True),
    "first_name":  fields.String,
    "last_name":   fields.String,
    "email":       fields.String,
    "created_at":  fields.String(readonly=True),
    "updated_at":  fields.String(readonly=True),
})

@api.route("/")
class UserList(Resource):
    @api.marshal_list_with(user_output, code=200)
    def get(self):
        return facade.list_users()  # Use Facade method

    @api.expect(user_input, validate=True)
    @api.marshal_with(user_output, code=201)
    def post(self):
        data = request.get_json(force=True) or {}
        try:
            created = facade.create_user(data)  # Use Facade method
        except ValueError as e:
            msg = str(e)
            if msg in ("email_already_exists", "missing_required_fields"):
                api.abort(400, msg)
            api.abort(400, msg)
        return created, 201


@api.route("/<string:user_id>")
@api.param("user_id", "The user ID")
class UserItem(Resource):
    @api.marshal_with(user_output, code=200)
    def get(self, user_id):
        u = facade.get_user(user_id)  # Use Facade method
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
        for bad in ("id", "password", "password_hash", "created_at", "updated_at", "is_admin"):
            updates.pop(bad, None)

        try:
            updated = facade.update_user(user_id, updates)  # Use Facade method
        except ValueError as e:
            if str(e) == "email_already_exists":
                api.abort(400, "email_already_exists")
            api.abort(400, str(e))
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
        if not facade.delete_user(user_id):  # Use Facade method
            api.abort(404, "User not found")
        return "", 204

