from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from sqlalchemy import create_engine
import os
from typing import Iterator

from dotenv import load_dotenv
load_dotenv()  # <-- добавь


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Create .env with DATABASE_URL=...")

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False,
                            autocommit=False, expire_on_commit=False, future=True)


class Base(DeclarativeBase):
    pass


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
