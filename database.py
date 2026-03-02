from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

# Define database file path
DB_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DB_DIR, "bank_statements.db")

# Create data directory if it doesn't exist
os.makedirs(DB_DIR, exist_ok=True)

# Create the SQLAlchemy engine
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, echo=False)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Creates all tables in the database (if they don't already exist).
    """
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized at {DB_PATH}")

def get_session():
    """
    Returns a new database session.
    """
    return SessionLocal()
