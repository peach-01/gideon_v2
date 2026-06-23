CREATE TABLE memory_evidence (
    id UUID PRIMARY KEY,

    memory_id UUID NOT NULL,

    message_id UUID,
    episode_id UUID,

    confidence FLOAT,

    created_at TIMESTAMP
);