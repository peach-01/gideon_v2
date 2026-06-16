CREATE TABLE memories (
    id UUID PRIMARY KEY,

    vector_id TEXT,

    memory_type TEXT NOT NULL,
    memory_tier TEXT NOT NULL,

    content TEXT,
    canonical_content TEXT NOT NULL,

    confidence FLOAT DEFAULT 1.0,
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

    metadata JSONB DEFAULT '{},'

    created_at TIMESTAMP,
    updated_at TIMESTAMP,

    CONSTRAINT uq_memories_canonical
    UNIQUE(canonical_content)
);

CREATE INDEX idx_memories_canonical
ON memories(canonical_content);

CREATE INDEX idx_memories_type
ON memories(memory_type);

CREATE INDEX idx_memories_tier
ON memories(memory_tier);

CREATE INDEX idx_memories_importance
ON memories(importance DESC);