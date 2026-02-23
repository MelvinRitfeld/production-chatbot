import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Read from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")


# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Base for models
Base = declarative_base()


def init_db() -> None:
    """
    Create tables if they do not exist.
    (Safe because you already use proper schema)
    """
    from . import models  # avoids circular import
    Base.metadata.create_all(bind=engine)