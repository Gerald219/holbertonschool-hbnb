"""Regression checks for configuration and isolation of the database."""
import pytest
from flask_jwt_extended import create_access_token, decode_token

from part3.app import create_app
from part3.app.extensions import db
from part3.config import TestConfig


def test_custom_jwt_secret_is_used_for_signing():
    class CustomConfig(TestConfig):
        JWT_SECRET_KEY = "custom-signing-key-for-this-test-123456789"

    app = create_app(CustomConfig)
    with app.app_context():
        token = create_access_token(identity="test-user")
        assert decode_token(token)["sub"] == "test-user"
    other_app = create_app(TestConfig)
    with other_app.app_context():
        from jwt.exceptions import InvalidSignatureError
        with pytest.raises(InvalidSignatureError):
            decode_token(token)


def test_database_is_isolated_from_development(app, setup_db):
    with app.app_context():
        assert db.engine.url.database == ":memory:"


@pytest.mark.parametrize("missing", ["JWT_SECRET_KEY", "SQLALCHEMY_DATABASE_URI"])
def test_missing_deployment_configuration_is_rejected(missing):
    config = type("IncompleteConfig", (TestConfig,), {missing: None})
    with pytest.raises(ValueError):
        create_app(config)
