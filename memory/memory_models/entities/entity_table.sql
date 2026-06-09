CREATE TABLE entities (
    id UUID PRIMARY KEY,

    name TEXT NOT NULL,
    entity_type TEXT NOT NULL,

    aliases JSONB,

    description TEXT,

    created_at TIMESTAMP,
    updated_at TIMESTAMP,
);

CREATE INDEX idx_entities_name
ON entities(name);

CREATE INDEX idx_entities_type
ON entities(entity_type);