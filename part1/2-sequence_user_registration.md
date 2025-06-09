<p align="center">
  <img src="https://img.shields.io/badge/Project-HBnB%20Part1-blue" />
  <img src="https://img.shields.io/badge/Assignment-Sequence%20Diagram-brightgreen" />
  <img src="https://img.shields.io/badge/API-User%20Registration-lightgrey" />
</p>

<h2 align="center"> Sequence Diagram: User Registration</h2>

---

<p align="center"><b> What This Diagram Explains</b></p>

<p align="center">
  This sequence diagram shows the step-by-step process the system follows when a new user registers.<br>
  The flow begins in the <strong>Presentation Layer</strong> (API & Services), continues through the <strong>Business Logic Layer</strong>,<br>
  and ends when the new user data is stored via the <strong>Persistence Layer</strong>.
</p>

---
# User Registration – Sequence Diagram

This diagram shows how a **new user signs up** in the HBNB system.  
It follows the request from the user's browser, through the API, to the logic and database — and back.

---

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
    API-->>User: 201 Created + user info# User Registration – Sequence Diagram

This diagram shows how a **new user signs up** in the HBNB system.  
It follows the request from the user's browser, through the API, to the logic and database — and back.

---

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
