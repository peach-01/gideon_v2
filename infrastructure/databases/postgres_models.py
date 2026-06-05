from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Float, DateTime, Boolean, Text, Integer


class Base(DeclarativeBase):
    pass


# ------------ MEMORIES ------------
class MemoryRecord(Base):

    __tablename__ = "memories"

    id = Column(String, primary_key=True)
    vector_id = Column(String)

    memory_type = Column(String)
    content = Column(String)

    confidence = Column(Float)
    importance = Column(Float)

    source = Column(String)

    created_at = Column(DateTime)
    last_accessed = Column(DateTime)

    access_count = Column(Integer)


# ------------ MESSAGES ------------
class MessageRecord(Base):

    __tablename__ = "messages"

    id = Column(String, primary_key=True)
    session_id = Column(String)

    role = Column(String)

    content = Column(String)

    timestamp = Column(DateTime)


# ------------ GOALS -------------
class GoalRecord(Base):

    __tablename__ = "goals"

    id = Column(String, primary_key=True)

    title = Column(String, nullable=False)
    description = Column(Text)

    status = Column(String, default="active")
    priority = Column(Float, default=0.5)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    completed_at = Column(DateTime, nullable=True)

    source = Column(String)


# ---------- CALENDAR EVENTS -----------
class EventRecord(Base):

    __tablename__ = "events"

    id = Column(String, primary_key=True)

    title = Column(String)

    start = Column(DateTime)
    end = Column(DateTime)


# ------------- REMINDERS --------------
class ReminderRecord(Base):

    __tablename__ = "reminders"

    id = Column(String, primary_key=True)

    title = Column(String)
    message = Column(String)

    due_at = Column(DateTime)

    completed = Column(Boolean)