CREATE TABLE memory_edges (

    id UUID PRIMARY KEY,

    source_entity_id UUID NOT NULL,
    target_entity_id UUID NOT NULL,

    relation TEXT NOT NULL,

    confidence FLOAT DEFAULT 1.0,

    origin_episode_id UUID,

    created_at TIMESTAMP,

    CONSTRAINT uq_relations
    UNIQUE(target_entity_id, relation, source_entity_id)
);

CREATE INDEX idx_edges_source
ON memory_edges(source_entity_id);

CREATE INDEX idx_edges_target
ON memory_edges(target_entity_id);

CREATE INDEX idx_edges_relation
ON memory_edges(relation);