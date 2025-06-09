<p align="center">
  <img src="https://img.shields.io/badge/Project-HBnB%20Part1-blue" />
  <img src="https://img.shields.io/badge/Assignment-Sequence%20Diagram-brightgreen" />
  <img src="https://img.shields.io/badge/API-Place%20Creation-lightgrey" />
</p>

<h2 align="center">Sequence Diagram: Place Creation</h2>

---

## Place Creation – Sequence Diagram

This diagram shows how a user creates a new place listing in the HBNB system.  
The request flows from the user's browser, through the API and services, into the business logic,  
and finally to the database where the new place record is stored.

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
    API->>Service: validate place data
    Service->>BusinessLogic: create_place()
    BusinessLogic->>DBStorage: insert place
    DBStorage->>Database: save to places table
    Database-->>DBStorage: confirmation
    DBStorage-->>BusinessLogic: return place object
    BusinessLogic-->>Service: send place data
    Service-->>API: build response
    API-->>User: 201 Created + place info
