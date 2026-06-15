CREATE TABLE facts (
    id UUID PRIMARY KEY,
    fact TEXT,
    confidence FLOAT,
    source TEXT,
    created_at TIMESTAMP
);