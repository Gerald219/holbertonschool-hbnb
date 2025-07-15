<p align="center">
  <img src="https://img.shields.io/badge/Database%20Table-User-blue?style=for-the-badge">
</p>

```mermaid
classDiagram
    class User {
        +string id
        +string first_name
        +string last_name
        +string email
        +string password
        +boolean is_admin
        +datetime created_at
        +datetime updated_at
    }
```
-   `id` is the unique identifier for each user and acts as the primary key.
    
-   `first_name` and `last_name` store the user’s personal name information.
    
-   `email` must be unique and is used to identify the user or log them in.
    
-   `password` holds the hashed version of the user’s real password.
    
-   `is_admin` is a true/false value that marks if the user is an admin.
    
-   `created_at` and `updated_at` record when the user was added and last changed.
 
```mermaid
classDiagram
    class Place {
        +string id
        +string name
        +string description
        +string city
        +integer price_per_night
        +float latitude
        +float longitude
        +string owner_id
        +datetime created_at
        +datetime updated_at
    }
```
-   `id` is the unique ID for each place.
    
-   `name` is the public title of the place.
    
-   `description` is a longer summary of what the place offers.
    
-   `city` stores the location name.
    
-   `price_per_night` shows how much it costs to stay there per night.
    
-   `latitude` and `longitude` are the GPS coordinates for the place.
    
-   `owner_id` links this place to a user who owns it.
    
-   `created_at` and `updated_at` track when the place was added and last modified.
---
```mermaid
classDiagram
    class Review {
        +string id
        +string text
        +string user_id
        +string place_id
        +datetime created_at
        +datetime updated_at
    }
```
-   `id` is the unique identifier for each review.
    
-   `text` holds the content of the review that the user wrote.
    
-   `user_id` connects this review to the user who wrote it.
    
-   `place_id` connects it to the place being reviewed.
    
-   `created_at` and `updated_at` record when the review was added and last changed.
---  
```mermaid
classDiagram
    class Amenity {
        +string id
        +string name
        +datetime created_at
        +datetime updated_at
    }
 ```
 -   `id` is the primary key that uniquely identifies each amenity.
    
-   `name` describes what the amenity is (wifi, parking, and more).
    
-   `created_at` marks when the amenity was added.
    
-   `updated_at` tracks the last time the amenity was edited.
---      
```mermaid
classDiagram
    class place_amenity {
        +string place_id
        +string amenity_id
    }

    Place "1" --> "*" place_amenity : links with
    Amenity "1" --> "*" place_amenity : links with
```
-   `place_id` connects this row to a place.
    
-   `amenity_id` connects this row to an amenity.
    
-   These two fields form a bridge — a **many-to-many** relationship.
    
-   This lets one place have many amenities, and one amenity belong to many places.
---
```mermaid
classDiagram
    class Review {
        +string id
        +string text
        +string user_id
        +string place_id
        +datetime created_at
        +datetime updated_at
    }

    User "1" --> "*" Review : writes
    Place "1" --> "*" Review : receives
```
-   `id` is the unique ID for the review.
    
-   `text` holds the feedback message or opinion.
    
-   `user_id` links to the user who wrote the review.
    
-   `place_id` connects the review to the place being reviewed.
    
-   `created_at` and `updated_at` track when the review was posted or changed.
    
-   Each user can write many reviews, and each place can receive many reviews.
---
### All Major **tables** Connected
```mermaid
classDiagram
    class User {
        +string id
        +string first_name
        +string last_name
        +string email
        +string password
        +boolean is_admin
        +datetime created_at
        +datetime updated_at
    }

    class Place {
        +string id
        +string name
        +string description
        +string city
        +int price_per_night
        +float latitude
        +float longitude
        +string owner_id
        +datetime created_at
        +datetime updated_at
    }

    class Review {
        +string id
        +string text
        +string user_id
        +string place_id
        +datetime created_at
        +datetime updated_at
    }

    class Amenity {
        +string id
        +string name
        +datetime created_at
        +datetime updated_at
    }

    class PlaceAmenity {
        +string place_id
        +string amenity_id
    }

    User "1" --> "*" Place : owns
    User "1" --> "*" Review : writes
    Place "1" --> "*" Review : has
    Place "*" --> "*" Amenity : linked via PlaceAmenity
```
# Relationships 
-   **User** connects to **Place** (a user can own places)
    
-   **User** connects to **Review** (a user can write multiple reviews)
    
-   **Place** connects to **Review** (a place can have many reviews)
    
-   **Place** connects to **Amenity** using a middle link (`PlaceAmenity`) to allow many-to-many features
---

