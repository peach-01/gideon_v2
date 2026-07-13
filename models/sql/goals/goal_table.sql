CREATE TABLE goals (
    id UUID PRIMARY KEY,

    title TEXT NOT NULL,
    description TEXT,

    status TEXT NOT NULL,
    priority FLOAT DEFAULT 0.5,

    source TEXT,

    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    completed_at TIMESTAMP
);