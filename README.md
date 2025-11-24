# rule: everything must be inside this bash block; anything outside is a mistake.

cd ~/holbertonschool-hbnb

cat << 'EOF' > README.md
<!-- anchor for "back to top" -->
<a id="readme-top"></a>

<p align="center">
  <img alt="Project: HBnB API" src="https://img.shields.io/badge/Project-HBnB%20API-blue">
  <img alt="Parts: 1, 2 & 3" src="https://img.shields.io/badge/Parts-1%2C%202%20%26%203-6c757d">
  <img alt="Architecture: REST" src="https://img.shields.io/badge/Architecture-REST-success">
  <img alt="Auth: JWT" src="https://img.shields.io/badge/Auth-JWT-orange">
  <img alt="ORM: SQLAlchemy" src="https://img.shields.io/badge/ORM-SQLAlchemy-yellow">
  <img alt="Tests: Pytest (21+)" src="https://img.shields.io/badge/Tests-Pytest%20(21%2B)-brightgreen">
  <img alt="Python: 3.10" src="https://img.shields.io/badge/Python-3.10-lightgrey">
  <img alt="OS: Ubuntu 20.04" src="https://img.shields.io/badge/OS-Ubuntu%2020.04-informational">
</p>

<h1 align="center">HBnB API — Parts 1, 2 & 3</h1>

<p align="center"><em>From basic JSON routes to full JWT auth + SQL database: users, places, amenities, and reviews all talking through one REST API.</em></p>

---

## Quick view

- One API, three stages of growth (Part 1 → Part 2 → Part 3)
- Users, Places, Amenities, Reviews are the main objects
- Part 1: simple Flask + JSON routes, no database
- Part 2: Flask-RESTX namespaces and a Facade layer (clean separation)
- Part 3: SQLAlchemy models, JWT auth, role-based access, and pytest tests

### Quick map of the three parts

| Part | Focus                        | Main tools                          | What you get                                   |
|------|-----------------------------|--------------------------------------|-----------------------------------------------|
| 1    | Basic API routes            | Flask, JSON                         | Simple endpoints that return hard-coded data  |
| 2    | REST design + Facade        | Flask-RESTX, Facade                 | Clean resource URLs and business-layer logic  |
| 3    | Auth + database + tests     | SQLAlchemy, JWT, Pytest, Migrations | Real DB, secure tokens, and verified behavior |

---

## Part 1 — Basic API & Namespaces

Part 1 is the starter version of the API:

- Simple Flask app
- Hard-coded JSON data (no database yet)
- Basic routes under `/api/v1/`

What you learn/practice:

- How to create a Flask app
- How to return JSON responses
- How to organize simple routes for status and basic objects

### How to run Part 1

From your project root:

    cd ~/holbertonschool-hbnb
    export FLASK_APP=app   # the simple version used in Part 1
    flask run

Typical curl test:

    curl http://127.0.0.1:5000/api/v1/status

You should get a small JSON response showing the API is alive.

<p align="right"><a href="#readme-top">back to top</a></p>

---

## Part 2 — Database, Models, Repositories

In Part 2, the API stops using “fake data” and switches to a real database powered by SQLAlchemy.  
This part explains how data is stored, saved, updated, and deleted.

### What this part adds

- Real database instead of in-memory lists
- SQLAlchemy models for:
  - User
  - Place
  - Review
- Repositories (Python classes) that act like “helpers” to talk to the database
- Migrations so the database structure can grow without losing data
- Automatic timestamps (`created_at` / `updated_at`)

---

### 1) The model files

These are Python classes mapped to database tables.  
They describe what fields each table has (id, name, email, etc.).

Examples of fields you now have:

- User: `first_name`, `last_name`, `email`, `password_hash`
- Place: `owner_id`, `price_per_night`, `description`, `latitude`, `longitude`
- Review: `user_id`, `place_id`, `text`

Every model inherits from a shared **BaseModel**, which gives:

- `id`
- `created_at`
- `updated_at`

This makes all tables consistent and easy to manage.

---

### 2) The repository classes

These are “database assistants”.  
Instead of writing SQL manually, the API calls repository functions like:

- `repo.create_user()`
- `repo.get_user_by_email()`
- `repo.create_place()`
- `repo.list_reviews()`
- `repo.update_review()`

The repository layer does 3 main things:

1. Validates incoming data  
2. Talks to SQLAlchemy  
3. Returns clean Python objects back to the API  

This keeps the API clean and readable.

---

### 3) Database migrations

Flask-Migrate creates migration files to update your database structure.

Commands used (Part 2 / first time setup):

    export FLASK_APP=part3.app:create_app
    flask db init          # only once
    flask db migrate -m "create tables"
    flask db upgrade

Migrations let you evolve the schema safely without losing existing data.

---

### 4) The app factory connects everything

The main function `create_app()` does the wiring:

- loads database
- registers models
- registers namespaces (`users`, `places`, `reviews`, `auth`)
- loads JWT
- sets app configuration

This keeps your project structured and avoids spaghetti code.

---

### What you can do after Part 2

- Store users in the database  
- Store places created by users  
- Store reviews made by guests  
- Read data back correctly  
- Update and delete items  
- Keep timestamps automatically  
- Run migrations safely  

Part 2 prepares the foundation for Part 3 (Auth + Protected Routes + Tests).

<p align="right"><a href="#readme-top">back to top</a></p>

---

## Part 3 — Auth, Protection & Tests

In Part 3, the API becomes “real-world ready”: users log in, get tokens, and only authorized people can create/update/delete data.  
We also add tests so we know everything works, not just “seems” to work.

### What this part adds

- Login endpoint that returns a **JWT token**
- Passwords stored as **secure hashes** (bcrypt)
- `is_admin` flag inside the JWT to control powers
- Protected routes for:
  - creating/updating/deleting places
  - creating/updating/deleting reviews
  - updating/deleting users
- Pytest test suite that checks all the rules

---

### How login and JWT work (plain language)

1. You send email + password to `/api/v1/auth/login`.
2. The API:
   - finds the user by email
   - checks password with bcrypt
   - builds a JWT token with:
     - `sub` → user id
     - `is_admin` → True/False
3. The API sends back something like:

       { "access_token": "long.jwt.string..." }

4. On the next requests, you send:

       Authorization: Bearer <token>

5. The decorators `@jwt_required()` and `get_jwt_identity()`:

   - read the token
   - reject bad/expired tokens
   - give your user id to the view
   - expose `is_admin` via `get_jwt()`

---

### Route protection rules (simple guide)

#### Users

- `POST /api/v1/users/`
  - open (no token) → register new user

- `PUT /api/v1/users/<user_id>`
  - needs JWT
  - allowed if:
    - you are that user, or
    - you are admin

- `DELETE /api/v1/users/<user_id>`
  - needs JWT
  - allowed if:
    - you are that user, or
    - you are admin

---

#### Places

- `GET /api/v1/places/`
  - open (no token) → list all places

- `POST /api/v1/places/`
  - needs JWT
  - `owner_id` = current user
  - normal validation: name, city, price, etc.

- `PUT /api/v1/places/<place_id>`
  - needs JWT
  - allowed if:
    - you are **owner** of that place, or
    - you are admin

- `DELETE /api/v1/places/<place_id>`
  - needs JWT
  - allowed if:
    - you are **owner** of that place, or
    - you are admin

---

#### Reviews

- `GET /api/v1/reviews/`
  - open (no token) → list all reviews

- `POST /api/v1/reviews/`
  - needs JWT
  - rules:
    - you cannot review your own place
    - one review per user per place
    - place must exist
  - `user_id` comes from the token, not from the payload

- `PUT /api/v1/reviews/<review_id>`
  - needs JWT
  - only the **author** can edit

- `DELETE /api/v1/reviews/<review_id>`
  - needs JWT
  - allowed if:
    - you are the **author**, or
    - you are admin

---

## Tests — what is checked (short cards)

All tests live under `part3/tests/`.

- `test_auth.py`
  - register a new user via `/users/`
  - reject duplicate emails
  - login returns a valid token
  - wrong password → 401

- `test_protected.py`
  - deny access without token
  - allow access with valid token
  - reject token with wrong signature
  - confirm `is_admin` claim is present in JWT

- `test_places.py`
  - a logged-in user can create a place
  - only owner/admin can update a place
  - only owner/admin can delete a place
  - using another user’s token gives 403

- `test_reviews.py`
  - guest user can create a review on someone else’s place
  - cannot review own place
  - cannot review same place twice
  - only author (or admin) can edit/delete
  - 404s when review or place doesn’t exist

These tests are your safety net.  
If `pytest -q` passes, the main behavior is correct.

---

## How to run everything (one-shot guide)

### 1) Go to the project and activate venv

    cd ~/holbertonschool-hbnb
    source .venv/bin/activate

### 2) Set environment variables for the app

    export FLASK_APP=part3.app:create_app
    export FLASK_ENV=development

### 3) Upgrade the database (create tables)

    flask db upgrade

This uses Alembic migrations to create the tables for:

- users
- places
- amenities
- reviews

### 4) Run all tests

    PYTHONPATH=$(pwd) pytest -q

If everything is correct, you should see something like:

    21 passed in XX.XXs

### 5) Start the API server

    flask run

By default, it listens on:

- Base URL: http://127.0.0.1:5000/
- API base: http://127.0.0.1:5000/api/v1/
- Swagger docs: http://127.0.0.1:5000/api/v1/docs

### 6) Quick manual test with curl (from another terminal)

From your project root:

    cd ~/holbertonschool-hbnb

Set some test credentials:

    EMAIL="you.$(date +%s)@example.com"
    PASSWORD="MyStrongPass123!"

Create a user:

    curl -X POST http://127.0.0.1:5000/api/v1/users/ \
      -H "Content-Type: application/json" \
      -d "{
        \"first_name\": \"Test\",
        \"last_name\": \"User\",
        \"email\": \"${EMAIL}\",
        \"password\": \"${PASSWORD}\"
      }"

Login and capture the token:

    TOKEN=$(curl -s -X POST http://127.0.0.1:5000/api/v1/auth/login \
      -H "Content-Type: application/json" \
      -d "{
        \"email\": \"${EMAIL}\",
        \"password\": \"${PASSWORD}\"
      }" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

Create a protected place:

    curl -X POST http://127.0.0.1:5000/api/v1/places/ \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer ${TOKEN}" \
      -d '{
        "name": "My Test Place",
        "city": "San Juan",
        "price_per_night": 100,
        "description": "Simple test place",
        "latitude": 18.4655,
        "longitude": -66.1057
      }'

If those commands work, your Part 3 setup (auth + DB + routes) is fully alive.

---

### three parts

**Part 1 — Basic API & Namespaces**

- Routes, resources, simple JSON responses
- Simple Flask app with hard-coded data

**Part 2 — Database, Models, Repositories**

- SQLAlchemy models for all entities
- Repository layer for clean DB access
- Migrations to grow your schema safely

**Part 3 — Auth, Protection & Tests**

- JWT login + `is_admin` claims
- Protected endpoints for create/update/delete
- `pytest` suite proving everything works

All three parts together give you a mini but realistic REST backend:  
iauthentication, authorization, database, and tests.

<p align="right"><a href="#readme-top">back to top</a></p>

