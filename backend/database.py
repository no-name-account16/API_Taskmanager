from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#  Database connection url - the database is stored locally
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

#  create new database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
