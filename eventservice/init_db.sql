CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO events (name) VALUES
    ('Festival A'),
    ('Festival B'),
    ('Festival C');
