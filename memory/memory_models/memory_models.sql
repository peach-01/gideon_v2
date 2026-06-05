CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    session_id TEXT,
    role TEXT,
    content TEXT,
    created_at TIMESTAMP
);

CREATE TABLE facts (
    id UUID PRIMARY KEY,
    fact TEXT,
    confidence FLOAT,
    source TEXT,
    created_at TIMESTAMP,
);

CREATE TABLE preferences (
    id UUID PRIMARY KEY,
    key TEXT,
    value TEXT,
)