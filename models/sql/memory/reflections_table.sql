CREATE TABLE reflections (

    id UUID PRIMARY KEY,

    content TEXT,

    source_memory_id UUID,

    confidence FLOAT,

    created_at TIMESTAMP
);