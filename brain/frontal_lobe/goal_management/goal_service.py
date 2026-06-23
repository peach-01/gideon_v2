import uuid

from datetime import datetime, UTC

from infrastructure.databases.postgres import SessionLocal
from infrastructure.databases.postgres_models import GoalRecord

from memory.memory_models.basic_memory.memory_type import MemoryType


class GoalService:

    def __init__(self, memory_service):
        self.memory = memory_service

    async def create_goal(self, title: str, description: str = "", priority: float = 0.8, source: str = "user"):
        db = SessionLocal()

        try:
            goal_id = str(uuid.uuid4())
            now = datetime.now(UTC)

            goal = GoalRecord(
                id=goal_id,
                title=title,
                description=description,
                status="active",
                priority=priority,
                source=source,
                created_at=now,
                updated_at=now,
            )

            db.add(goal)
            db.commit()

            # store goal as permanent memory
            await self.memory.store(
                content=f"Goal: {title}",
                memory_type=MemoryType.GOAL,
                source="goal_service",
                importance=priority,
            )

            return goal
        
        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    async def update_goal(self, goal_id: str, **updates):
        db = SessionLocal()

        try:
            goal = db.query(GoalRecord).filter(GoalRecord.id == goal_id).first()
            if not goal:
                return None
            
            for key, val in updates.items():
                if hasattr(goal, key):
                    setattr(goal, key, val)

            goal.updated_at = datetime.now(UTC)

            db.commit()

            return goal

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    async def list_goals(self, active_only: bool = False):
        db = SessionLocal()

        try:
            q = db.query(GoalRecord)

            if active_only:
                q = q.filter(GoalRecord.status == "active")

            return q.order_by(GoalRecord.priority.desc()).all()

        finally:
            db.close()

    async def complete_goal(self, goal_id: str):
        db = SessionLocal()

        try:
            goal = db.query(GoalRecord).filter(GoalRecord.id == goal_id).first()
            if not goal:
                return None

            now = datetime.now(UTC)

            goal.status = "completed"
            goal.completed_at = now
            goal.updated_at = now

            db.commit()

            return goal

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()
            
