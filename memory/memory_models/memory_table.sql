CREATE TABLE memories (
    id UUID PRIMARY KEY,
    vector_id TEXT,
    memory_type TEXT,
    content TEXT,
    confidence FLOAT,
    source TEXT,
    created_at TIMESTAMP
);