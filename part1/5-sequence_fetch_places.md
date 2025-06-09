<p align="center">
  <img src="https://img.shields.io/badge/Project-HBnB%20Part1-blue" />
  <img src="https://img.shields.io/badge/Assignment-Sequence%20Diagram-brightgreen" />
  <img src="https://img.shields.io/badge/API-Fetch%20Places-lightgrey" />
</p>

<h2 align="center">Sequence Diagram: Fetching a List of Places</h2>

This diagram shows how the system handles a user’s request to retrieve a list of places.  
It goes step-by-step through the layers — starting with the API, then service logic, and finally pulling data from the database.

```mermaid
sequenceDiagram
    participant User
    participant API
    participant Service
    participant BusinessLogic
    participant DBStorage
    participant Database

    User->>API: GET /places?city=SanJuan
    API->>Service: forward request
    Service->>BusinessLogic: fetch_places(city="SanJuan")
    BusinessLogic->>DBStorage: query places
    DBStorage->>Database: SELECT * FROM places WHERE city = 'SanJuan'
    Database-->>DBStorage: matching places
    DBStorage-->>BusinessLogic: list of place objects
    BusinessLogic-->>Service: return results
    Service-->>API: format into JSON
    API-->>User: 200 OK + list of places
