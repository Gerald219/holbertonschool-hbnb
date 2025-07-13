from business.base_model import BaseModel
import bcrypt

class User(BaseModel):
    def __init__(self, **kwargs):
        self.first_name = kwargs.get("first_name", "")
        self.last_name = kwargs.get("last_name", "")
        self.email = kwargs.get("email", "")
        password = kwargs.get("password", "")
        if password and not password.startswith("$2b$"):
            self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        else:
            self.password = password
        super().__init__(**kwargs)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password.encode())
