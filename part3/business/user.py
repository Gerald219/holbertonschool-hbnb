from app.extensions import db
from business.base_model import BaseModel
import bcrypt

class User(BaseModel, db.Model):
    __tablename__ = "users"
    BaseModel.configure_fields(db)

    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        password = kwargs.get("password", "")
        if password and not password.startswith("$2b$"):
            self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        else:
            self.password = password
        self.first_name = kwargs.get("first_name", "")
        self.last_name = kwargs.get("last_name", "")
        self.email = kwargs.get("email", "")
        self.is_admin = kwargs.get("is_admin", False)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password.encode())
