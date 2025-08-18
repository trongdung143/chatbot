from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config.database import DATABASE_URL

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    access_token = Column(String)
    refresh_token = Column(String)
