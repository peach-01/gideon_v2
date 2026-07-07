import uuid
import json
from datetime import datetime, UTC
from sqlalchemy import or_

from infrastructure.databases.postgres import SessionLocal
from infrastructure.databases.postgres_models import MessageRecord

from memory.long_term_memory.episodic_memory.conversations.conversation_models.converstation_message import ConversationMessage
from memory.long_term_memory.episodic_memory.conversations.conversation_models.content_block import ContentBlock


class ConversationService:

    async def store_message(self, session_id: str, message: ConversationMessage):
        db = SessionLocal()

        for record in db.query(MessageRecord).all():

            try:
                json.loads(record.content)

            except Exception:

                record.content = json.dumps([
                    {
                        "type": "text",
                        "content": record.content
                    }
                ])

        try:
            message_id = str(uuid.uuid4())

            db.add(
                MessageRecord(
                    id=message_id,
                    session_id=session_id,
                    content=json.dumps([
                        block.to_dict()
                        for block in message.content
                    ]),
                    timestamp=datetime.now(UTC),
                )
            )

            db.commit()
        
        finally:
            db.close()

        return message_id
    

    def get_last_messages(self, session_id: str, limit: int=20):
        db = SessionLocal()

        try:
            msgs = []

            rows = db.query(MessageRecord).filter(MessageRecord.session_id == session_id)\
                .order_by(MessageRecord.timestamp.desc()).limit(limit).all()
            
            for row in reversed(rows):
                blocks = [
                    ContentBlock(**block)
                    for block in json.loads(row.content)
                ]

                msgs.append(
                    ConversationMessage(
                        role=row.role,
                        content=blocks,
                    )
                )
            
            return list(msgs)
        
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