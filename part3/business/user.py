from business.base_model import BaseModel
from app import db
import bcrypt

class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

