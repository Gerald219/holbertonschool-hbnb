```mermaid
erDiagram
    USERS ||--o{ PLACES : owns
    USERS ||--o{ REVIEWS : writes
    PLACES ||--o{ REVIEWS : "has"
    PLACES }o--o{ AMENITIES : "offers"
    PLACES }o--o{ PLACE_AMENITY : includes
    AMENITIES }o--o{ PLACE_AMENITY : belongs

