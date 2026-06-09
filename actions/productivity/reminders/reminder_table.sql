CREATE TABLE reminders (
    id UUID PRIMARY KEY,
    title TEXT,
    message TEXT,
    due_at TIMESTAMP,
    completed BOOLEAN
);