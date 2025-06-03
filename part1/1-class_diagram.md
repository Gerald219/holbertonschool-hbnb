![Project](https://img.shields.io/badge/Project-HBnB%20Part1-blue)
![Assignment](https://img.shields.io/badge/Assignment-Detailed%20Class%20Diagram-brightgreen)
![Layer](https://img.shields.io/badge/Layer-Business%20Logic-orange)

# Detailed Class Diagram


```mermaid
classDiagram

%% === BaseModel ===
class BaseModel {
    +UUID id
    +datetime created_at
    +datetime updated_at
    +save()
    +to_dict()
}

%% === User ===
class User {
    +string first_name
    +string last_name
    +string email
    +string password
    +bool is_admin
    +update_profile()
}

%% === Place ===
class Place {
    +string title
    +string description
    +float price
    +float latitude
    +float longitude
    +UUID user_id
    +publish()
}

%% === Review ===
class Review {
    +int rating
    +string comment
    +UUID user_id
    +UUID place_id
    +submit()
}

%% === Amenity ===
class Amenity {
    +string name
    +string description
    +bool is_active
    +toggle_active()
    +describe()
}

%% === Inheritance ===
BaseModel <|-- User
BaseModel <|-- Place
BaseModel <|-- Review
BaseModel <|-- Amenity

%% === Relationships ===
User "1" --> "*" Place : owns
User "1" --> "*" Review : writes
Place "1" --> "*" Review : receives
Place "1" --> "*" Amenity : has
Review "*" --> "1" Place : about
Review "*" --> "1" User : by
```i

![Class Diagram](./class_diagram.png)

---
---

## Entity Notes

### User

**Attributes**
- `first_name` *(string)* — User's first name
- `last_name` *(string)* — User's last name
- `email` *(string)* — Email address (used for login and communication)
- `password` *(string)* — Encrypted password for authentication
- `is_admin` *(bool)* — Flag indicating admin privileges

**Methods**
- `update_profile()` — Update the user's personal information

---

### Place

**Attributes**
- `title` *(string)* — Title of the place listing
- `description` *(string)* — Description of the space
- `price` *(float)* — Cost per night
- `latitude` *(float)* — Geo-location latitude
- `longitude` *(float)* — Geo-location longitude
- `user_id` *(UUID)* — Reference to the user who created the place

**Methods**
- `publish()` — Make the place publicly available

---

### Review

**Attributes**
- `rating` *(int)* — Star rating given by the user
- `comment` *(string)* — Written feedback about a place
- `user_id` *(UUID)* — Reference to the user who wrote the review
- `place_id` *(UUID)* — Reference to the place being reviewed

**Methods**
- `submit()` — Save and validate the review

---

### Amenity

**Attributes**
- `name` *(string)* — Name of the amenity (e.g., Wi-Fi)
- `description` *(string)* — Optional longer explanation of the amenity
- `is_active` *(bool)* — Whether the amenity is currently available

**Methods**
- `toggle_active()` — Enable or disable the amenity
- `describe()` — Return formatted description for display

---

### Class Explanations

**BaseModel**  
This is the main “template” for every class. It gives each object:  
- A unique ID  
- Timestamps to track when it was made and last changed  
- Functions to save itself or convert the object to a dictionary  

**User**  
Represents someone using the app. Each user:  
- Can own places  
- Can write reviews  
- Can be marked as admin or regular  
- Has a first name, last name, email, and password  
- Can update their profile

flowchart TD
    A[User] --> B[Has first name, last name, email, password]
    A --> C[Can update their profile]
    A --> D[Can be marked as admin or regular]
    A --> E[Can own places]
    A --> F[Can write reviews]

**Place**  
Represents a property (house or apartment):  
- Belongs to a user 
- Has a title, description, price, and location  
- Stores latitude and longitude to show location of property
- Can be reviewed and have amenities  
- Can be published using a method  

flowchart TD
    A[Place Class] -->|user_id| B(Belongs to a user)
    A -->|title, description, price, location| C(Has main details)
    A -->|latitude and longitude| D(Stores coordinates)
    A -->|reviews| E(Can be reviewed)
    A -->|amenities| F(Can have amenities)
    A -->|publish method| G(Can be published)

**Review**  
This is a comment left by a user about a place. It:  
- Includes a rating and a comment  
- Links to both the user and the place  
- Can be submitted using a method  

flowchart TD
    A[Review Class]

    A --> R1[rating: score given to place]
    A --> R2[comment: written feedback]
    A --> R3[user_id: who wrote the review]
    A --> R4[place_id: place being reviewed]
    A --> R5[submit method: submits the review]

**Amenity**  
An extra feature a place has attached to It:  
- Has a name and description  
- Can be marked as active or inactive  
- Has a method to turn it on or off  
- Has a method to describe itself  

flowchart TD
    A[Amenity Class]

    A --> AM1[name: name of the amenity]
    A --> AM2[description: what it is or does]
    A --> AM3[is_active: marks if amenity is available]
    A --> AM4[toggle_active: turns the amenity on/off]
    A --> AM5[describe: returns a description of the amenity]

**Inheritance**  
All classes inherit from **BaseModel**. This means they:  
- Automatically get a unique ID  
- Have timestamps for creation and updates  
- Can save themselves  
- Can be converted to dictionaries 
