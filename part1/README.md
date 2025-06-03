## **Part 1: Technical Documentation**

This part focuses on designing the core structure of the HBnB Evolution application. It includes:

- A **high-level package diagram** showing the three-layer architecture (Presentation, Business Logic, Persistence) and how they interact using the facade pattern.
- A **detailed class diagram** for the Business Logic layer, covering the main entities: User, Place, Review, and Amenity — with all attributes, methods, and relationships (including inheritance).
- A section with **class explanations** that describe what each class does, what attributes it holds, and how the classes are connected.
- These diagrams and notes lay the foundation for how the app will work internally and guide the implementation in later parts of the project.

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
