from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL (replace with your actual database URL)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:HelloHackers1994%40%2A@localhost:5432/oil-gas-db"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()