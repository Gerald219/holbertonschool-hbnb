# HBnB API

This is a simple REST API for a booking platform that manages users, places, and reviews.

## Endpoints
- **/api/v1/auth/login** - Login and get a JWT token
- **/api/v1/users** - User operations (GET, POST, PUT, DELETE)
- **/api/v1/places** - Place operations (GET, POST, PUT, DELETE)
- **/api/v1/reviews** - Review operations (POST, PUT, DELETE)

## Technologies Used
- Flask
- Flask-RESTX
- Flask-JWT-Extended
- SQLAlchemy
- Bcrypt
- Flask-Migrate

## How to Run
1. Clone the repository: `git clone https://github.com/your-repository-link.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up the database: `flask db upgrade`
4. Run the app: `flask run`
5. Access the API: `http://127.0.0.1:5001`


## Part 3 – Auth, Database & Tests

This part connects the API to a real database and protects it with JWT.

- ✅ JWT-based authentication (`/api/v1/auth/login`) with bcrypt-hashed passwords
- ✅ SQLAlchemy models + repositories for `User`, `Place`, and `Review`
- ✅ Role-based access using an `is_admin` claim in the JWT
- ✅ Protected endpoints for creating places, linking amenities, and writing reviews
- ✅ Pytest suite that checks authentication, protected routes, place rules, and review rules  
  (local run: `PYTHONPATH=$(pwd) pytest -q` → currently **21 tests passed**)

### How to run Part 3 locally

```bash
cd ~/holbertonschool-hbnb
source .venv/bin/activate  # if you use a virtualenv
export FLASK_APP=part3.app:create_app
export FLASK_ENV=development
flask run

-API base URL: http://127.0.0.1:5000/api/v1/

-Swagger docs: http://127.0.0.1:5000/api/v1/docs

