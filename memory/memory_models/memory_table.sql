CREATE TABLE memories (
    id UUID PRIMARY KEY,
    vector_id TEXT,

    memory_type TEXT,
    content TEXT,
    canonical_content TEXT,

    confidence FLOAT,
    source TEXT,
    
    created_at TIMESTAMP
    last_accessed TIMESTAMP,

    access_count INTEGER DEFAULT 0
);

CREATE INDEX idx_memories_canonical
ON memories(canonical_content);