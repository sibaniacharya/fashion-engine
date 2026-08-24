from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Connect to Postgres if deployed, otherwise fallback to local SQLite
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

is_sqlite = not DATABASE_URL
engine_url = DATABASE_URL or "sqlite:///./discovery_engine.db"

# SQLite requires specific connect_args, Postgres does not
connect_args = {"check_same_thread": False} if is_sqlite else {}

engine = create_engine(engine_url, connect_args=connect_args)
    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
