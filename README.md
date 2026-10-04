# HBnB — accommodation REST API

A Holberton School coursework project that develops an accommodation API in stages: architecture diagrams, an in-memory prototype, and a database-backed Flask API. The current implementation is in **Part 3**.

## What this project demonstrates

- Python REST endpoints for users, places, amenities, and reviews.
- SQLAlchemy models, SQLite persistence, and Alembic migrations.
- Bcrypt password hashing and JWT login.
- Owner, author, and administrator checks for protected actions.
- Automated API tests for registration, login, place ownership, and reviews.

This is an educational backend project. It does not include a booking/payment system or a finished customer-facing website.

## Run locally

Requirements: Python 3.12 and a terminal. Run these commands from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
flask --app part3.app:create_app db upgrade
flask --app part3.app:create_app run --port 5001
```

Open [the interactive API docs](http://127.0.0.1:5001/docs) or [the health endpoint](http://127.0.0.1:5001/). API routes start with `/api/v1`.

The database is created at `hbnb_dev.db` by default. It is excluded from Git. For a development server with automatic reload, use `bash scripts/frun.sh`. Set `PORT` to choose another port.

## Try registration and login

With the server running in another terminal:

```bash
curl -X POST http://127.0.0.1:5001/api/v1/users/ \
  -H 'Content-Type: application/json' \
  -d '{"first_name":"Demo","last_name":"User","email":"demo@example.com","password":"ExamplePassword123!"}'

curl -X POST http://127.0.0.1:5001/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"demo@example.com","password":"ExamplePassword123!"}'
```

Use the returned `access_token` as `Authorization: Bearer <token>` for protected endpoints. Password hashes are not returned in user responses.

## Test

```bash
python -m pytest -q
```

Tests create a fresh **in-memory SQLite database** for each test. They do not reset the development database. The GitHub Actions workflow runs this same command on pushes and pull requests.

## Repository guide

| Directory | Purpose |
| --- | --- |
| `part1/` | Package, class, and request-sequence diagrams |
| `part2/` | Earlier Flask prototype with in-memory repositories |
| `part3/presentation/` | REST endpoints and authorization checks |
| `part3/business/` | Facade and business objects |
| `part3/models/` | SQLAlchemy database models |
| `part3/persistence/` | Database repository operations |
| `part3/tests/` | API and configuration regression tests |
| `migrations/` | Versioned database schema |
| `scripts/` | Development launcher and optional HTTP smoke checks |

## Configuration and current limits

- `DATABASE_URL` overrides the development database location.
- `JWT_SECRET_KEY` sets the signing key. Without it, development generates a temporary random key; tokens stop working after a server restart. Set a persistent secret through the environment when needed.
- `ADMIN_EMAILS` is a comma-separated administrator allowlist. Leave it unset for ordinary local testing.
- `ProdConfig` requires `DATABASE_URL` and `JWT_SECRET_KEY`; it does not supply deployment credentials. Select it explicitly with `create_app(ProdConfig)` when wiring a production server.
- Part 2 is retained to show the earlier learning stage, including its simplified password handling. Use Part 3 for the current demonstration.
- Further work includes stricter input validation, pagination, deployment hardening, and a frontend. Passing the test suite does not establish production readiness.
- `scripts/smoke_e2e.sh` is an optional local exercise that creates demo records and expects `owner@test` to have administrator access. Use only with a disposable local database; the isolated pytest suite is the default check.

## Author and related work

[Gerald Mulero (@Gerald219)](https://github.com/Gerald219)

Other coursework examples: [C shell](https://github.com/Gerald219/holbertonschool-simple_shell), [sorting algorithms](https://github.com/Gerald219/holbertonschool-sorting_algorithms), and [binary trees](https://github.com/Gerald219/holbertonschool-binary_trees).
