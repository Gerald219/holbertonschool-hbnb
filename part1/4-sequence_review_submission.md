<p align="center">
  <img src="https://img.shields.io/badge/Project-HBnB%20Part1-blue" />
  <img src="https://img.shields.io/badge/Assignment-Sequence%20Diagram-brightgreen" />
  <img src="https://img.shields.io/badge/API-Review%20Submission-lightgrey" />
</p>

<h2 align="center">Sequence Diagram: Review Submission</h2>

This diagram shows how a user submits a review for a place in the HBNB system.  
The request goes through the API and backend logic, then stores the review in the database.

```mermaid
sequenceDiagram
    participant User
    participant API
    participant Service
    participant BusinessLogic
    participant DBStorage
    participant Database

    User->>API: POST /reviews (place_id, rating, comment)
    API->>Service: verify user identity & route request
    Service->>Service: check place exists & validate content
    Service->>BusinessLogic: create_review(place_id, rating, comment)
    BusinessLogic->>DBStorage: prepare review & insert into storage
    DBStorage->>Database: write review to reviews table
    Database-->>DBStorage: confirm save was successful
    DBStorage-->>BusinessLogic: return stored review object
    BusinessLogic-->>Service: send back completed review data
    Service-->>API: package response with status
    API-->>User: 201 Created + review details
