from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from genetics.base_configs.config import settings

engine = create_engine(settings.POSTGRES_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)