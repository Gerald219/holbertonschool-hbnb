from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from part3.app.extensions import bcrypt
from part3.models import User
import os


api = Namespace("auth", description="Authentication", path="/auth")

login_input = api.model("LoginInput", {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
})

login_output = api.model("LoginOutput", {
    "access_token": fields.String,
})

    @api.expect(login_input, validate=True)
    @api.marshal_with(login_output, code=200)
    def post(self):
        data = request.get_json(force=True) or {}
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        # Find user in DB
        user = User.query.filter(User.email == email).first()
        if not user:
            api.abort(401, "Invalid credentials")

        # Check bcrypt password hash
        if not user.password_hash or not bcrypt.check_password_hash(user.password_hash, password):
            api.abort(401, "Invalid credentials")

        # Admin claim
        admin_emails = {e.strip().lower() for e in os.getenv("ADMIN_EMAILS", "").split(",") if e.strip()}
        is_admin = bool(getattr(user, "is_admin", False)) or (email in admin_emails)

        token = create_access_token(identity=user.id, additional_claims={"is_admin": is_admin})
        return {"access_token": token}, 200

