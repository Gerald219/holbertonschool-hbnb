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

INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '001-gerald',
    'Gerald',
    'Mulero',
    'gdmasm@gmail.com',
    '$2b$12$6VYpUcRWR7Rb4spDPZgRtuF3RPjhUXINRoXibCCw8Fq8NdAN/3r4q',
    TRUE,
    DATETIME('now'),
    DATETIME('now')
);

INSERT INTO amenities (id, name, created_at, updated_at) VALUES
('amenity-001', 'Wi-Fi', DATETIME('now'), DATETIME('now')),
('amenity-002', 'Air Conditioning', DATETIME('now'), DATETIME('now')),
('amenity-003', 'Swimming Pool', DATETIME('now'), DATETIME('now')),
('amenity-004', 'Washer/Dryer', DATETIME('now'), DATETIME('now')),
('amenity-005', 'Parking', DATETIME('now'), DATETIME('now'));
