from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from part3.persistence.user_storage import repo
from part3.business.user import User as DomainUser
import os


api = Namespace("auth", description="Authentication", path="/auth")

login_input = api.model("LoginInput", {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
})

login_output = api.model("LoginOutput", {
    "access_token": fields.String,
})

@api.route("/login")
class Login(Resource):
    @api.expect(login_input, validate=True)
    @api.marshal_with(login_output, code=200)
    def post(self):
        data = request.get_json(force=True) or {}
        email = data.get("email")
        password = data.get("password")

        #  find user by email (scan-in-memory store)
        users = repo.get_all("users") or []
        match = next((u for u in users if u.get("email") == email), None)
        if not match:
            api.abort(401, "Invalid credentials")
        
        #  rebuild domain user - check hashed password
        du = DomainUser(**match)
        if not du.check_password(password):
            api.abort(401, "Invalid credentials")
        
        # build token claims from env guest listemails and is_admin flag
        admin_emails = {
            e.strip().lower()
            for e in os.getenv("ADMIN_EMAILS", "").split(",")
            if e.strip()
        }
        is_admin = bool(match.get("is_admin", False)) or (email and email.lower() in admin_emails)

        # identity is the user id + is_admin flag in token
        token = create_access_token(
            identity=match["id"],
            additional_claims={"is_admin": bool(is_admin)}
        )
        return {"access_token": token}, 200
