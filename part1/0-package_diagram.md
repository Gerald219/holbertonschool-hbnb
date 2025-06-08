![Project](https://img.shields.io/badge/Project-HBnB%20Part1-blue)
![Assignment](https://img.shields.io/badge/Assignment-High--Level%20Package%20Diagram-brightgreen)
![Layer](https://img.shields.io/badge/Layer-All%20Layers-orange)

# High-Level Package Diagram

```mermaid

classDiagram

class PresentationLayer {
    +API
    +Services
}

class BusinessLogicLayer {
    +User
    +Place
    +Review
    +Amenity
}

class PersistenceLayer {
    +FileStorage
    +DBStorage
    +Database
}

PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Data Access

```

---


# Class Explanations
## Presentation Layer
### API  
The entry point of the app. It:
- Receives requests from the user or front-end
- Forwards them to the right service or logic
- Returns a structured response (usually JSON)

```mermaid
flowchart TD
    A[API] --> A1[Receives user request]
    A --> A2[Processes routes]
    A --> A3[Sends to Business Logic Layer]
    A --> A4[Returns structured response]
```

---
### Services  
These are the backend helpers that do the actual work after the API receives a request. Services:
- Take requests from the API and break them into logic operations
- Call the appropriate functions in the Business Logic Layer
- Handle data formatting, response generation, and sometimes validation

```mermaid
flowchart TD
    S[Services] --> S1[Triggered by API request]
    S --> S2[Calls logic-layer functions]
    S --> S3[Formats response]
    S --> S4[Returns result to API]
```

---
## Business Logic Layer  
### User  
Represents a person using the platform.  
- Can own one or many places  
- Can write reviews for places  
- Has personal info like name, email, password  
- May have admin privileges  
- Can update their profile

```mermaid
flowchart TD
    U[User] --> U1[Owns places]
    U --> U2[Writes reviews]
    U --> U3[Has name, email, password]
    U --> U4[Can be admin]
    U --> U5[Can update profile]
```
---

### Place  
Represents a property that a user can list on the platform.  
- Belongs to a specific user (the owner)  
- Has details like title, description, price, and location  
- Includes geographic data: latitude and longitude  
- Can be reviewed by other users  
- Can have connected amenities  
- Can be published for others to see

```mermaid
flowchart TD
    P[Place] --> P1[Owned by a user]
    P --> P2[Has title, description, price, location]
    P --> P3[Includes latitude and longitude]
    P --> P4[Can be reviewed]
    P --> P5[Can have amenities]
    P --> P6[Can be published]
```
---
 ### Review  
Represents feedback that a user gives about a place.  
- Includes a rating (score) and a written comment  
- Connected to the user who wrote it  
- Linked to the place it describes  
- Helps other users decide whether to visit a place  
- Can be submitted and stored as part of the system

```mermaid
flowchart TD
    R[Review] --> R1[Has rating and comment]
    R --> R2[Linked to a user]
    R --> R3[Linked to a place]
    R --> R4[Submitted by user]
    R --> R5[Helps inform other users]
```
---

### Amenity  
Represents a feature or service that a place offers.  
- Has a name and short description  
- Can be active or inactive (turned on or off)  
- Used to describe what makes a place more comfortable or useful  
- Helps users filter or choose places with certain features  
- Can be managed by the place owner

```mermaid
flowchart TD
    A[Amenity] --> A1[Has name and description]
    A --> A2[Can be active or inactive]
    A --> A3[Describes place features]
    A --> A4[Used in search or filters]
    A --> A5[Managed by owner]
```

---
## Persistence Layer
### FileStorage  
Stores and retrieves objects using local files.  
- Saves objects (like users or places) into a `.json` file  
- Converts objects into text format and writes them to disk  
- Can reload the file and turn it back into Python objects  
- Used for development, testing, or when no real database is set up

```mermaid
flowchart TD
    FS[FileStorage] --> FS1[Save as JSON]
    FS --> FS2[Write to local file]
    FS --> FS3[Read file into memory]
    FS --> FS4[Used for local development]
```

---
### DBStorage  
Connects the app to a real database system.  
- Stores objects like users or places as rows in database tables  
- Uses SQL to create, read, update, or delete data  
- Converts Python objects into database-friendly formats and back  
- Used in production when working with large or shared data

```mermaid
flowchart TD
    DB[DBStorage] --> DB1[Map object to table row]
    DB --> DB2[Run SQL queries]
    DB --> DB3[Save and load from database]
    DB --> DB4[Used in production setups]
```

---
### Database  
Stores all the application data in structured tables.  
- Holds permanent records for users, places, reviews, and more  
- Organizes data using tables, rows, and columns  
- Only accessed through `DBStorage`, not directly by the app  
- Makes it possible to search, filter, and manage large sets of data

```mermaid
flowchart TD
    DB[Database] --> DB1[Stores data in tables]
    DB --> DB2[Contains rows and columns]
    DB --> DB3[Accessed by DBStorage]
    DB --> DB4[Holds all persistent records]

