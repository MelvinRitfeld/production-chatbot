from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from db.models import Base

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)