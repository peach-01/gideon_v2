import uuid

from datetime import datetime, UTC

from infrastructure.databases.postgres import SessionLocal
from infrastructure.databases.postgres_models import GoalRecord

from models.python.memory.enums.memory_type import MemoryType
from models.python.goals.goal_summary import GoalSummary


class GoalManager:

    def __init__(self, memory_service):
        self.memory = memory_service


    async def boot(self):
        await self.get_active_goals()
        print("[GOAL-MANAGER] Ready.")


    # -------- GETTERS --------
    async def get_goal(self, goal_id: str):
        db = SessionLocal()
        
        try:
            return db.query(GoalRecord).filter(GoalRecord.id == goal_id).first()
        
        finally:
            db.close()


    async def get_active_goals(self):
        db = SessionLocal()
        
        try:
            return db.query(GoalRecord).filter(GoalRecord.status == "active").order_by(GoalRecord.priority.desc()).all()

        finally:
            db.close()


    async def get_summary(self) -> GoalSummary:
        active_goals = await self.get_active_goals()

        db = SessionLocal()
        try:
            total = db.query(GoalRecord).count()

            completed = db.query(GoalRecord).filter(GoalRecord.status == "completed").count()

        finally:
            db.close()

        highest_priority = active_goals[0].title if active_goals else None

        return GoalSummary(
            active=[goal.title for goal in active_goals],
            completed=completed,
            highest_priority=highest_priority,
            total=total,
        )
    

    # -------- CREATE ---------
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


    # -------- UPDATE ---------
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
            

    async def set_active(self, goal_id: str):
        db = SessionLocal()

        try:
            goal = db.query(GoalRecord).filter(GoalRecord.id == goal_id).first()

            if not goal:
                return None

            goal.status = "active"
            goal.updated_at = datetime.now(UTC)

            db.commit()
            return goal

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()


    async def archive_completed(self):
        db = SessionLocal()

        try:
            goals = db.query(GoalRecord).filter(GoalRecord.status == "completed").all()

            now = datetime.now(UTC)

            for goal in goals:
                goal.status = "archived"
                goal.updated_at = now

            db.commit()

            return len(goals)

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()


