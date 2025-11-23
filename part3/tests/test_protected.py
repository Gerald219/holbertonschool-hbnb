import uuid

import pytest
from flask import Flask
from part3.app import create_app
from part3.app.extensions import db


## build app + DB per test file

@pytest.fixture
def app():
    ## normal app, but in testing mode
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    ## HTTP client to hit endpoints
    return app.test_client()


@pytest.fixture
def setup_db(app):
    ## start each test with a clean DB
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield db
    ## tear down DB after tests
    with app.app_context():
        db.session.remove()
        db.drop_all()


## helpers

def _unique_email() -> str:
    ## avoid clashes with old rows
    return f"testuser_{uuid.uuid4().hex}@example.com"


## tests: register + login flow

def test_register_new_user_success(client, setup_db):
    ## happy path: new user registers
    email = _unique_email()
    payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": email,
        "password": "MyStrongPass123!",
    }

    ## real endpoint: POST /api/v1/users/
    resp = client.post("/api/v1/users/", json=payload)
    assert resp.status_code in (200, 201)

    data = resp.get_json()
    assert data is not None
    assert "id" in data
    assert data["email"] == email
    ## passwords never come back
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_email_rejected(client, setup_db):
    ## same email twice should fail on second try
    email = _unique_email()
    payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": email,
        "password": "MyStrongPass123!",
    }

    first = client.post("/api/v1/users/", json=payload)
    assert first.status_code in (200, 201)

    second = client.post("/api/v1/users/", json=payload)
    assert second.status_code in (400, 409)

    data = second.get_json()
    error_text = (data.get("message") or "").lower()
    assert "email" in error_text
    assert "exists" in error_text or "already" in error_text


def test_login_success_returns_token(client, setup_db):
    ## register then login and expect a token
    email = _unique_email()
    password = "MyStrongPass123!"

    register_payload = {
        "first_name": "Login",
        "last_name": "User",
        "email": email,
        "password": password,
    }
    reg_resp = client.post("/api/v1/users/", json=register_payload)
    assert reg_resp.status_code in (200, 201)

    login_payload = {"email": email, "password": password}
    login_resp = client.post("/api/v1/auth/login", json=login_payload)
    assert login_resp.status_code == 200

    data = login_resp.get_json()
    ## we only care that some token field exists
    assert any(key in data for key in ("access_token", "token", "jwt", "access"))


def test_login_with_bad_password_fails(client, setup_db):
    ## login with wrong password must fail
    email = _unique_email()
    password = "MyStrongPass123!"

    register_payload = {
        "first_name": "Bad",
        "last_name": "Password",
        "email": email,
        "password": password,
    }
    reg_resp = client.post("/api/v1/users/", json=register_payload)
    assert reg_resp.status_code in (200, 201)

    bad_login_payload = {"email": email, "password": "WrongPass999!"}
    login_resp = client.post("/api/v1/auth/login", json=bad_login_payload)
    assert login_resp.status_code in (400, 401, 403)

    data = login_resp.get_json()
    msg = (data.get("message") or "").lower()
    ## message should clearly say creds are bad
    assert "invalid" in msg or "credentials" in msg or "password" in msg

