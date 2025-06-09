

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
```

---

## Class Explanations

### BaseModel  
The main “template” for all classes. It gives:
- A unique ID  
- Creation and update timestamps  
- Methods to save or convert to dictionary

---

### User  
Represents someone using the app. A user:
- Has name, email, password  
- Can be marked as admin  
- Can update their profile  
- Can own places and write reviews  

```mermaid
flowchart TD
    U[User] --> U1[Has first name, last name, email, password]
    U --> U2[Can update profile]
    U --> U3[Can be marked admin]
    U --> U4[Can own places]
    U --> U5[Can write reviews]
```

---

### Place  
Represents a property (house or apartment). It:
- Belongs to a user  
- Has title, description, price, and location  
- Stores latitude and longitude  
- Can be reviewed  
- Can have amenities  
- Can be published  

```mermaid
flowchart TD
    P[Place] --> P1[Belongs to a user]
    P --> P2[Has title, description, price, location]
    P --> P3[Has coordinates: latitude and longitude]
    P --> P4[Can be reviewed]
    P --> P5[Can have amenities]
    P --> P6[Can be published]
```

---

### Review  
A comment a user leaves about a place. It:
- Has a rating and comment  
- Links to both user and place  
- Can be submitted  

```mermaid
flowchart TD
    R[Review]
    R --> R1[Rating - score given to place]
    R --> R2[Comment - written feedback]
    R --> R3[User ID - who wrote the review]
    R --> R4[Place ID - place being reviewed]
    R --> R5[Submit method]
```

---

### Amenity  
A feature or service offered at a place. It:
- Has a name and description  
- Can be active or inactive  
- Can describe itself  
- Can be turned on/off  

```mermaid
flowchart TD
    A[Amenity] --> A1[Name: name of the amenity]
    A --> A2[Description: what it does]
    A --> A3[is_active: shows if it's available]
    A --> A4[Toggle: turns amenity on/off]
    A --> A5[Describe method]
```

---
### Inheritance

All classes inherit from `BaseModel`, meaning they:

- Automatically get ID and timestamps  
- Have `save()` and `to_dict()` methods  

---

### Relationships

This section shows how the main classes interact:

- Users can own places  
- Users can write reviews  
- Places can have reviews  
- Places can have amenities  
- Each review is written by a user and is about one place  

```mermaid
classDiagram
    User "1" --> "*" Place : owns
    User "1" --> "*" Review : writes
    Place "1" --> "*" Review : receives
    Place "1" --> "*" Amenity : has
    Review "*" --> "1" Place : about
    Review "*" --> "1" User : by
