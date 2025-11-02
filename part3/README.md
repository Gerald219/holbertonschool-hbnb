<p align="center">
  <img src="https://img.shields.io/badge/HBnB-REST%20API-blueviolet" alt="HBnB REST API Badge" />
</p>

# HBnB Evolution – RESTful API

This is a web API, this allows to create, read, update, and delete Users, Places, Amenities, and Reviews — just like Airbnb platform.

Built for the Holberton School project **HBNB Evolution**, it follows clear, simple REST rules so it's easy to use, test, and build on.

---
###  Project Structure

Here’s how the folders are organized — kind of like labeled drawers in a file cabinet:

```plaintext
part2/
├── app.py                  ← Main file that runs the API server
├── presentation/           ← All routes (like doors into the app)
│   ├── users.py
│   ├── places.py
│   ├── amenities.py
│   └── reviews.py
├── business/               ← Logic brain (how data is handled)
│   └── models/             ← Each data type (User, Place, etc.)
├── persistence/            ← Memory drawer (saves the info)
│   └── repository.py
└── test_models.py          ← Test script to make sure models work
```

Real-life analogy:
Imagine a hotel:

- `presentation/` = the front desk and website (how people interact)
- `business/` = the manager making decisions (what happens behind the scenes)
- `persistence/` = the file cabinet where guest records are stored

---

## Installation

To run this REST API on your local machine, follow these steps:

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/holbertonschool-hbnb.git
   cd holbertonschool-hbnb/part2

 2. (Optional) Set up a virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install project dependencies
pip install -r requirements.txt

4. Run the API server
python3 app.py

*5. Open your browser to test the API:**  
use link: [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs) to try out the endpoints and explore the interactive documentation.

---

### Usage

Once the server is running, you can test the API using:

- `curl` commands in your terminal (examples below)
- Browsing `/docs` for interactive testing via Swagger UI

#### Example: Create a new user

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{"first_name": "Alice", "last_name": "Smith", "email": "alice@example.com", "password": "secret"}'
```

---

### API Endpoints

Here are the main routes you can interact with:

#### Users
- `GET /api/v1/users/` — list all users  
- `POST /api/v1/users/` — create a new user  
- `GET /api/v1/users/<user_id>` — retrieve a user  
- `PUT /api/v1/users/<user_id>` — update a user  
- `DELETE /api/v1/users/<user_id>` — remove a user  

####  Places
- `GET /api/v1/places/`  
- `POST /api/v1/places/`  
- `GET /api/v1/places/<place_id>`  
- `PUT /api/v1/places/<place_id>`  

#### Amenities
- `GET /api/v1/amenities/`  
- `POST /api/v1/amenities/`  
- `GET /api/v1/amenities/<amenity_id>`  
- `PUT /api/v1/amenities/<amenity_id>`  

#### Reviews
- `GET /api/v1/reviews/`  
- `POST /api/v1/reviews/`  
- `GET /api/v1/reviews/<review_id>`  
- `PUT /api/v1/reviews/<review_id>`  
- `DELETE /api/v1/reviews/<review_id>`  

---

### Built With

- Python 3  
- Flask + Flask-RESTx  
- RESTful Architecture  
- Swagger UI (auto-docs at `/docs`)  

---

### Author

Project built by **Gerald Mulero** for Holberto Coding School.
