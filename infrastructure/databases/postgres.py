from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from genetics.base_configs.config import settings
from infrastructure.databases.postgres_models import Base

engine = create_engine(settings.POSTGRES_URL)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)