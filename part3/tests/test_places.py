import uuid

import pytest
from part3.app import create_app
from part3.app.extensions import db


## app + DB fixtures

@pytest.fixture
def app():
    ## real app in testing mode
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    ## HTTP client to call API
    return app.test_client()


@pytest.fixture
def setup_db(app):
    ## clean DB before each test module
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield db
    with app.app_context():
        db.session.remove()
        db.drop_all()


## helpers

def _unique_email() -> str:
    return f"place_tester_{uuid.uuid4().hex}@example.com"


def _register_user(client, email=None, password="MyStrongPass123!"):
    if email is None:
        email = _unique_email()
    payload = {
        "first_name": "Place",
        "last_name": "Tester",
        "email": email,
        "password": password,
    }
    resp = client.post("/api/v1/users/", json=payload)
    assert resp.status_code in (200, 201)
    return resp.get_json()


def _login(client, email, password):
    resp = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200
    data = resp.get_json()
    return data.get("access_token")


def _create_place(client, token, overrides=None):
    """Create a simple place owned by the token user."""
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": "Test Place",
        "city": "San Juan",
        "price_per_night": 100,
        "description": "Test description",
    }
    if overrides:
        payload.update(overrides)
    resp = client.post("/api/v1/places/", json=payload, headers=headers)
    assert resp.status_code in (200, 201)
    return resp.get_json()


## tests


def test_get_unknown_place_returns_404(client, setup_db):
    """GET on a random place id should return 404."""
    resp = client.get("/api/v1/places/does-not-exist")
    assert resp.status_code == 404


def test_owner_can_update_their_place(client, setup_db):
    """Owner should be able to update their own place."""
    email = _unique_email()
    password = "MyStrongPass123!"
    user = _register_user(client, email=email, password=password)
    token = _login(client, email, password)

    place = _create_place(client, token)
    place_id = place["id"]

    headers = {"Authorization": f"Bearer {token}"}
    resp = client.put(
        f"/api/v1/places/{place_id}",
        json={"price_per_night": 150, "name": "Updated Name"},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["price_per_night"] == 150
    assert data["name"] == "Updated Name"


def test_non_owner_cannot_update_place(client, setup_db):
    """Another normal user should get 403 when updating someone else’s place."""
    password = "MyStrongPass123!"
    owner = _register_user(client, password=password)
    other = _register_user(client, password=password)

    owner_token = _login(client, owner["email"], password)
    other_token = _login(client, other["email"], password)

    place = _create_place(client, owner_token)
    place_id = place["id"]

    headers = {"Authorization": f"Bearer {other_token}"}
    resp = client.put(
        f"/api/v1/places/{place_id}",
        json={"name": "Hacked Name"},
        headers=headers,
    )
    assert resp.status_code == 403


def test_owner_can_delete_place(client, setup_db):
    """Owner should be able to delete their place and then get 404 on GET."""
    email = _unique_email()
    password = "MyStrongPass123!"
    user = _register_user(client, email=email, password=password)
    token = _login(client, email, password)

    place = _create_place(client, token)
    place_id = place["id"]

    headers = {"Authorization": f"Bearer {token}"}
    delete_resp = client.delete(f"/api/v1/places/{place_id}", headers=headers)
    assert delete_resp.status_code == 204 or delete_resp.status_code == 200

    get_resp = client.get(f"/api/v1/places/{place_id}")
    assert get_resp.status_code == 404


def test_non_owner_cannot_delete_place(client, setup_db):
    """Another normal user should not be able to delete a place they don’t own."""
    password = "MyStrongPass123!"
    owner = _register_user(client, password=password)
    other = _register_user(client, password=password)

    owner_token = _login(client, owner["email"], password)
    other_token = _login(client, other["email"], password)

    place = _create_place(client, owner_token)
    place_id = place["id"]

    headers = {"Authorization": f"Bearer {other_token}"}
    resp = client.delete(f"/api/v1/places/{place_id}", headers=headers)
    assert resp.status_code == 403

