from typing import Dict, Any
from part3.persistence.sql_repository import SQLAlchemyRepository  # SQLAlchemy-backed user repo


class Facade:
    """Thin business layer that talks to the SQLAlchemy repo."""

    def __init__(self):
        ## one repo instance for all user calls
        self.repo = SQLAlchemyRepository()

    def test_connection(self):
        """Quick smoke test helper, not used by API tests."""
        return self.repo.create_user({
            "first_name": "Test",
            "email": "test@example.com",
            "password": "test1234",
        })

    def create_user(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user in the database."""
        return self.repo.create_user(payload)

    def list_users(self):
        """Return all users."""
        return self.repo.list_users()

    def get_user(self, user_id: str):
        """Return a single user by id."""
        return self.repo.get_user(user_id)

    def update_user(self, user_id: str, updates: Dict[str, Any]):
        """Update a user."""
        return self.repo.update_user(user_id, updates)

    def delete_user(self, user_id: str) -> bool:
        """Delete a user by id."""
        return self.repo.delete_user(user_id)

