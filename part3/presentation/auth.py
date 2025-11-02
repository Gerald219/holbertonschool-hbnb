from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from part3.persistence.repository import InMemoryRepository
from part3.business.user import User as DomainUser


api = Namespace("auth", description="Authentication", path="/auth")
repo = InMemoryRepository()

login_input = api.model("LoginInput", {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
})

login_output = api.model("LoginOutput", {
    "access_token": fields.String,
})
