CREATE TABLE memory_edges (
    id UUID PRIMARY KEY,

    source_entity UUID REFERENCES entities(id),
    relation TEXT,
    target_entity UUID REFERENCES entities(id),

    confidence FLOAT,

    created_at TIMESTAMP
);

CREATE INDEX idx_edges_source
ON memory_edges(source_entity);

CREATE INDEX idx_edges_relation
ON memory_edges(relation)

CREATE INDEX idx_edges_target
ON memory_edges(target_entity)