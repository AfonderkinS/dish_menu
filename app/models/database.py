from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "sqlite:///D:\PythonProject\dish_menu\app\localdb.db"

engine = create_engine(DATABASE_URL, echo=False, future=True)
session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()