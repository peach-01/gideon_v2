CREATE TABLE memories (
    id UUID PRIMARY KEY,

    vector_id TEXT,

    memory_type TEXT,

    content TEXT,
    canonical_content TEXT NOT NULL,

    confidence FLOAT,
    importance FLOAT DEFAULT 0.5,
    stability FLOAT DEFAULT 1.0,

    source TEXT,
    
    last_accessed TIMESTAMP,
    access_count INTEGER DEFAULT 0,

    -- provenance (origins for traceablity)
    origin_message_id UUID,
    origin_episode_id UUID,
    origin_memory_id UUID,

    root_memory_id UUID,

    valid_from TIMESTAMP,
    valid_until TIMESTAMP,

    created_at TIMESTAMP,
    updated_at TIMESTAMP,

    CONSTRAINT uq_memories_canonical
    UNIQUE(canonical_content)
);

CREATE INDEX idx_memories_canonical
ON memories(canonical_content);