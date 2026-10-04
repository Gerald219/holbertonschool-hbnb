"""Shared fixtures use a fresh in-memory database, never the development DB."""
import pytest

from part3.app import create_app
from part3.app.extensions import db
from part3.config import TestConfig


@pytest.fixture
def app(monkeypatch):
    monkeypatch.delenv("ADMIN_EMAILS", raising=False)
    return create_app(TestConfig)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def setup_db(app):
    with app.app_context():
        db.create_all()
    yield db
    with app.app_context():
        db.session.remove()
        db.drop_all()
