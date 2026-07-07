CREATE TABLE memory_lineage (
    id UUID PRIMARY KEY,

    child_memory_id UUID NOT NULL,
    parent_memory_id UUID NOT NULL,

    relationship_type TEXT NOT NULL,

    created_at TIMESTAMP
);