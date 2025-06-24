from persistence.repository import InMemoryRepository

class Facade:
    def __init__(self):
        self.repo = InMemoryRepository()

    def test_connection(self):
        return self.repo.save("users", {
            "first_name": "Test",
            "email": "test@example.com"
        })
