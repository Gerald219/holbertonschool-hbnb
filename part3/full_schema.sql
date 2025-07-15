CREATE TABLE reviews (
    id VARCHAR(60) PRIMARY KEY,
    text VARCHAR(1024) NOT NULL,
    user_id VARCHAR(60) NOT NULL,
    place_id VARCHAR(60) NOT NULL,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (place_id) REFERENCES places(id)
);

CREATE TABLE amenities (
    id VARCHAR(60) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    created_at DATETIME,
    updated_at DATETIME
);

CREATE TABLE place_amenity (
    place_id VARCHAR(60),
    amenity_id VARCHAR(60),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);
