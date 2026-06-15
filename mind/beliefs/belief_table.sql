CREATE TABLE beliefs (

    id UUID PRIMARY KEY,

    statement TEXT,

    confidence FLOAT,
    stability FLOAT,

    domain TEXT,
    source TEXT,

    evidence JSONB,
    contradictions JSONB,

    last_reviewed TIMESTAMP,

    valid_from TIMESTAMP,
    valid_until TIMESTAMP,
    
    created_at TIMESTAMP
);