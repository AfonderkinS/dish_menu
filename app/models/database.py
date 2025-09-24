from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session


BASE_DIR = Path(__file__).resolve().parent.parent

DB_NAME = "localdb.db"

DATABASE_URL = f"sqlite:///{BASE_DIR}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

Base = declarative_base()

def init_db() -> None:
    Base.metadata.create_all(engine)


def drop_db() -> None:
    Base.metadata.drop_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
