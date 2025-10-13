<p align="center">
  <img src="https://img.shields.io/badge/Project-HBnB%20Part1-blue" />
  <img src="https://img.shields.io/badge/Assignment-Sequence%20Diagram-brightgreen" />
  <img src="https://img.shields.io/badge/API-Place%20Creation-lightgrey" />
</p>

<h2 align="center">Sequence Diagram: Place Creation</h2>

This diagram shows how a user creates a new place listing in the HBNB system.  
It traces the full path from the front-end request, through the layers of the application, down to the database.

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
