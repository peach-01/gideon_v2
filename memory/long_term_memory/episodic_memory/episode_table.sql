CREATE TABLE episodes (

    id UUID PRIMARY KEY,

    summary TEXT,

    session_id TEXT,

    start_time TIMESTAMP,
    end_time TIMESTAMP,

    emotional_weight FLOAT,
    importance FLOAT,

    embedding_id TEXT,

    parent_episode_id UUID,

    created_at TIMESTAMP
);