import uuid

import pytest
from part3.app import create_app
from part3.app.extensions import db


@pytest.fixture
def app():
    ## normal app, in testing mode
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def setup_db(app):
    ## fresh DB per module
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield db
    with app.app_context():
        db.session.remove()
        db.drop_all()


def _unique_email(prefix="reviews") -> str:
    return f"{prefix}_{uuid.uuid4().hex}@example.com"


def _register_user(client, email=None, password="MyStrongPass123!"):
    if email is None:
        email = _unique_email()
    payload = {
        "first_name": "Reviewer",
        "last_name": "User",
        "email": email,
        "password": password,
    }
    resp = client.post("/api/v1/users/", json=payload)
    assert resp.status_code in (200, 201)
    return resp.get_json()


def _login(client, email, password):
    resp = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200
    return resp.get_json()["access_token"]


def _create_place(client, token, overrides=None):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": "Reviewable Place",
        "city": "San Juan",
        "price_per_night": 120,
        "description": "Review me",
    }
    if overrides:
        payload.update(overrides)
    resp = client.post("/api/v1/places/", json=payload, headers=headers)
    assert resp.status_code in (200, 201)
    return resp.get_json()


def _create_review(client, token, place_id, text="Nice stay"):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"text": text, "place_id": place_id}
    resp = client.post("/api/v1/reviews/", json=payload, headers=headers)
    return resp


def test_create_review_requires_auth(client, setup_db):
    """POST /reviews/ without JWT should be rejected."""
    resp = client.post("/api/v1/reviews/", json={"text": "Hi", "place_id": "x"})
    assert resp.status_code in (401, 422)


def test_user_can_review_someone_elses_place(client, setup_db):
    """User B can review a place owned by user A."""
    password = "MyStrongPass123!"

    # owner creates place
    owner = _register_user(client, password=password)
    owner_token = _login(client, owner["email"], password)
    place = _create_place(client, owner_token)
    place_id = place["id"]

    # reviewer logs in and reviews the place
    reviewer = _register_user(client, password=password)
    reviewer_token = _login(client, reviewer["email"], password)

    resp = _create_review(client, reviewer_token, place_id, text="Great spot!")
    assert resp.status_code in (200, 201)
    data = resp.get_json()
    assert data["place_id"] == place_id
    assert data["user_id"] == reviewer["id"]
    assert data["text"] == "Great spot!"


def test_cannot_review_own_place(client, setup_db):
    """Owner should not be able to review their own place."""
    password = "MyStrongPass123!"
    owner = _register_user(client, password=password)
    owner_token = _login(client, owner["email"], password)
    place = _create_place(client, owner_token)
    place_id = place["id"]

    resp = _create_review(client, owner_token, place_id, text="I love my own place")
    assert resp.status_code == 403


def test_cannot_review_same_place_twice(client, setup_db):
    """Same user cannot review the same place twice."""
    password = "MyStrongPass123!"
    owner = _register_user(client, password=password)
    owner_token = _login(client, owner["email"], password)
    place = _create_place(client, owner_token)
    place_id = place["id"]

    reviewer = _register_user(client, password=password)
    reviewer_token = _login(client, reviewer["email"], password)

    first = _create_review(client, reviewer_token, place_id, text="First review")
    assert first.status_code in (200, 201)

    second = _create_review(client, reviewer_token, place_id, text="Second review")
    assert second.status_code == 409


def test_only_author_can_update_review(client, setup_db):
    """Non-author should get 403 when trying to edit a review."""
    password = "MyStrongPass123!"
    owner = _register_user(client, password=password)
    owner_token = _login(client, owner["email"], password)
    place = _create_place(client, owner_token)
    place_id = place["id"]

    author = _register_user(client, password=password)
    author_token = _login(client, author["email"], password)
    review_resp = _create_review(client, author_token, place_id, text="Editable text")
    review = review_resp.get_json()
    review_id = review["id"]

    other = _register_user(client, password=password)
    other_token = _login(client, other["email"], password)

    headers = {"Authorization": f"Bearer {other_token}"}
    resp = client.put(
        f"/api/v1/reviews/{review_id}",
        json={"text": "Hacked"},
        headers=headers,
    )
    assert resp.status_code == 403


def test_author_can_update_review_text(client, setup_db):
    """Author can change their review text."""
    password = "MyStrongPass123!"
    owner = _register_user(client, password=password)
    owner_token = _login(client, owner["email"], password)
    place = _create_place(client, owner_token)
    place_id = place["id"]

    author = _register_user(client, password=password)
    author_token = _login(client, author["email"], password)
    review_resp = _create_review(client, author_token, place_id, text="Old text")
    review = review_resp.get_json()
    review_id = review["id"]

    headers = {"Authorization": f"Bearer {author_token}"}
    resp = client.put(
        f"/api/v1/reviews/{review_id}",
        json={"text": "New text"},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["text"] == "New text"


def test_author_can_delete_review(client, setup_db):
    """Author should be able to delete their own review."""
    password = "MyStrongPass123!"
    owner = _register_user(client, password=password)
    owner_token = _login(client, owner["email"], password)
    place = _create_place(client, owner_token)
    place_id = place["id"]

    author = _register_user(client, password=password)
    author_token = _login(client, author["email"], password)
    review_resp = _create_review(client, author_token, place_id, text="Delete me")
    review = review_resp.get_json()
    review_id = review["id"]

    headers = {"Authorization": f"Bearer {author_token}"}
    delete_resp = client.delete(f"/api/v1/reviews/{review_id}", headers=headers)
    assert delete_resp.status_code in (200, 204)

    get_resp = client.get(f"/api/v1/reviews/{review_id}")
    assert get_resp.status_code == 404


def test_non_author_cannot_delete_review(client, setup_db):
    """Non-author, non-admin should get 403 when deleting a review."""
    password = "MyStrongPass123!"
    owner = _register_user(client, password=password)
    owner_token = _login(client, owner["email"], password)
    place = _create_place(client, owner_token)
    place_id = place["id"]

    author = _register_user(client, password=password)
    author_token = _login(client, author["email"], password)
    review_resp = _create_review(client, author_token, place_id, text="Do not touch")
    review = review_resp.get_json()
    review_id = review["id"]

    other = _register_user(client, password=password)
    other_token = _login(client, other["email"], password)

    headers = {"Authorization": f"Bearer {other_token}"}
    resp = client.delete(f"/api/v1/reviews/{review_id}", headers=headers)
    assert resp.status_code == 403

