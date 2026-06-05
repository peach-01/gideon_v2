import uuid
from datetime import datetime, UTC
from sqlalchemy import or_

from infrastructure.databases.postgres import SessionLocal
from infrastructure.databases.postgres_models import MessageRecord


class ConversationService:

    async def store_message(self, session_id: str, role: str, content: str):
        db = SessionLocal()

        try:
            db.add(MessageRecord(
                id=str(uuid.uuid4()),
                session_id=session_id,
                role=role,
                content=content,
                timestamp=datetime.now(UTC),
            ))

            db.commit()
        
        finally:
            db.close()

    def get_last_messages(self, session_id: str, limit: int=20):
        db = SessionLocal()

        try:
            rows = db.query(MessageRecord).filter(MessageRecord.session_id == session_id)\
                .order_by(MessageRecord.timestamp.desc()).limit(limit).all()
            
            return list(reversed(rows))
        
        finally:
            db.close()

    def search_conversations(self, query: str, session_id: str | None = None, limit: int = 200):
        db = SessionLocal()

        try:
            terms = [
                t.strip() for t in query.split()
                if len(t.strip()) > 2
            ]

            q = db.query(MessageRecord)

            if session_id:
                q = q.filter(MessageRecord.session_id == session_id)

            if terms:
                q = q.filter(or_(*[
                    MessageRecord.content.ilike(f"%{term}%")
                    for term in terms
                ]))

            return q.order_by(MessageRecord.timestamp.desc()).limit(limit).all()

        finally:
            db.close()