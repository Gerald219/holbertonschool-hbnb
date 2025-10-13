<p align="center">
  <img src="https://img.shields.io/badge/Project-HBnB%20Part1-blue" />
  <img src="https://img.shields.io/badge/Assignment-Sequence%20Diagram-brightgreen" />
  <img src="https://img.shields.io/badge/API-User%20Registration-lightgrey" />
</p>

<h2 align="center">Sequence Diagram: User Registration</h2>

---

## User Registration – Sequence Diagram

This diagram shows how a **new user signs up** in the HBNB system.  
It follows the request from the user's browser, through the API, to the logic and database — and back.

---

## What This Diagram Explains

This sequence diagram shows the step-by-step process the system follows when a new user registers.  
The flow begins in the **Presentation Layer** (API & Services), continues through the **Business Logic Layer**,  
and ends when the new user data is stored in the **Persistence Layer**.

---

## Mermaid Diagram

```mermaid
sequenceDiagram
    participant User
    participant API
    participant Service
    participant BusinessLogic
    participant DBStorage
    participant Database

    User->>API: POST /register
    API->>Service: validate input
    Service->>BusinessLogic: create_user()
    BusinessLogic->>DBStorage: insert user
    DBStorage->>Database: save to users table
    Database-->>DBStorage: confirmation
    DBStorage-->>BusinessLogic: return user object
    BusinessLogic-->>Service: send user data
    Service-->>API: build response
    API-->>User: 201 Created + user info
