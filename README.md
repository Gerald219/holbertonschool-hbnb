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

