from business.base_model import BaseModel

class User(BaseModel):
    def __init__(self, **kwargs):
        self.first_name = kwargs.get("first_name", "")
        self.last_name = kwargs.get("last_name", "")
        self.email = kwargs.get("email", "")
        self.password = kwargs.get("password", "")
        super().__init__(**kwargs)
