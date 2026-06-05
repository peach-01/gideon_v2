CREATE TABLE messages (
    id UUID PRIMARY KEY,
    session_id TEXT,
    role TEXT,
    content TEXT,
    timestamp TIMESTAMP
);