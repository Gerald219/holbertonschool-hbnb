from part3.business.base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    def __init__(self, **kwargs):
        self.first_name = kwargs.get("first_name", "")
        self.last_name = kwargs.get("last_name", "")
        self.email = kwargs.get("email", "")

        self.password_hash = kwargs.get("password_hash")
        super().__init__(**kwargs)

    def set_password(self, plain_password: str) -> None:
        """Hash and store the password (will not be shown)."""
        if plain_password:
            self.password_hash = generate_password_hash(plain_password)
    
    def check_password(self, plain_password: str) -> bool:
        """Verify a plain password against the stored hash."""
        return bool(self.password_hash) and check_password_hash(self.password_hash, plain_password)
