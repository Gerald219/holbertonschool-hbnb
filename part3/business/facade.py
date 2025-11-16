from persistence.sql_repository import SQLAlchemyRepository  # Import the SQLAlchemyRepository

class Facade:
    def __init__(self):
        self.repo = SQLAlchemyRepository()  # Use the SQLAlchemy-based repository instead of InMemoryRepository

    def test_connection(self):
        return self.repo.create_user({
            "first_name": "Test",
            "email": "test@example.com",
            "password": "test1234"  # Make sure to include the password field as required
        })

    def create_user(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user in the database"""
        return self.repo.create_user(payload)

