from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = "sqlite:///D:/PythonProject/dish_menu/app/localdb.db"

engine = create_engine(DATABASE_URL, echo=False, future=True)
session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def init_db() -> None:
    Base.metadata.create_all(engine)


def drop_db() -> None:
    Base.metadata.drop_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    session = session_local()
    try:
        yield session
    finally:
        session.close()