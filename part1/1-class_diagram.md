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

**Place**  
Represents a property (house or apartment):  
- Belongs to a user 
- Has a title, description, price, and location  
- Stores latitude and longitude to show location of property
- Can be reviewed and have amenities  
- Can be published using a method  

**Review**  
This is a comment left by a user about a place. It:  
- Includes a rating and a comment  
- Links to both the user and the place  
- Can be submitted using a method  

**Amenity**  
An extra feature a place has attached to It:  
- Has a name and description  
- Can be marked as active or inactive  
- Has a method to turn it on or off  
- Has a method to describe itself  

**Inheritance**  
All classes inherit from **BaseModel**. This means they:  
- Automatically get a unique ID  
- Have timestamps for creation and updates  
- Can save themselves  
- Can be converted to dictionaries 
