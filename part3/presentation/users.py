from flask import request
from flask_restx import Namespace, Resource, fields
from part3.persistence.user_storage import repo
from part3.business.user import User as DomainUser

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
    "first_name":  fields.String(required=False),
    "last_name":   fields.String(required=False),
    "email":       fields.String(required=False),
    "password":    fields.String(required=False),
})


@api.route("/")
class UserList(Resource):
    @api.marshal_list_with(user_output, code=200)
    def get(self):
        return repo.get_all("users")

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_output, code=201)
    def post(self):
        data = request.json or {}
        plain = data.pop("password", None)
        if not plain:
            api.abort(400, "Password is required")

        user = DomainUser(**data)
        user.set_password(plain)

        record = {
            "id":user.id,
            "first_name":user.first_name,
            "last_name":user.last_name,
            "email":user.email,
            "password_hash":user.password_hash,
            "created_at":str(user.created_at),
            "updated_at":str(user.updated_at),
        }
        created = repo.save("users", record)
        return created, 201


@api.route("/<string:user_id>")
@api.param("user_id", "The user ID")
class UserItem(Resource):
    @api.marshal_with(user_output, code=200)
    def get(self, user_id):
        user = repo.get("users", user_id)
        if not user:
            api.abort(404, "User not found")
        return user

    @api.expect(user_update, validate=True)
    @api.marshal_with(user_output, code=200)
    def put(self, user_id):
        updates = request.json or {}
        updates.pop("password", None)  # plain password not accepted here
        updated_user = repo.update("users", user_id, updates)
        if not updated_user:
            api.abort(404, "User not found")
        return updated_user

    def delete(self, user_id):
        api.abort(405, "DELETE not supported for users in Part 3")
