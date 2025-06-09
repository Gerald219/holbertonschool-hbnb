<p align="center">
  <img src="https://img.shields.io/badge/Project-HBnB%20Part1-blue" />
  <img src="https://img.shields.io/badge/Assignment-Sequence%20Diagram-brightgreen" />
  <img src="https://img.shields.io/badge/API-Place%20Creation-lightgrey" />
</p>

<h2 align="center"> Sequence Diagram: Place Creation </h2>

---

# Place Creation – Sequence Diagram

This diagram shows how a **user creates a new place listing** in the HBNB system.  
It traces the full path from the front-end request, through the layers of the application, down to the database.

---

```mermaid
sequenceDiagram
    participant User
    participant API
    participant Service
    participant BusinessLogic
    participant DBStorage
    participant Database

    User->>API: POST /places
    API->>Service: check authentication
    Service->>Service: validate listing data
    Service->>BusinessLogic: create_place(title, description, price...)
    BusinessLogic->>DBStorage: insert new place
    DBStorage->>Database: write to places table
    Database-->>DBStorage: confirm write
    DBStorage-->>BusinessLogic: place object
    BusinessLogic-->>Service: pass place object
    Service-->>API: prepare response
    API-->>User: 201 Created + place details
---

### What This Diagram Explains

This sequence diagram shows how the system handles the process when a user creates a new place listing.

It walks through each step — starting from the API receiving a request, all the way through saving the place to the database and returning a response.

---

- **User → API:**  
  The user sends a `POST /places` request with the listing information (title, description, price, location, etc).

- **API → Service:**  
  The API checks authentication and forwards the request to the service layer.

- **Service → Service (self-call):**  
  The service validates the listing data to make sure everything is correct.

- **Service → BusinessLogic:**  
  If valid, the service calls the logic layer to create the new `Place` object.

- **BusinessLogic → DBStorage:**  
  The logic prepares the object and asks the storage system to save it.

- **DBStorage → Database:**  
  The storage layer writes the place data into the `places` table.

- **Database → DBStorage:**  
  The database confirms the operation was successful.

- **DBStorage → BusinessLogic:**  
  The storage layer returns the saved place with its ID and timestamps.

- **BusinessLogic → Service:**  
  The logic passes the complete place object to the service layer.

- **Service → API → User:**  
  The API returns a `201 Created` response with the new place info.

---
