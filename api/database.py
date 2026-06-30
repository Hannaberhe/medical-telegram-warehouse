"""Database connection using SQLAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/medical_warehouse')

try:
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    print("Database connected")
except Exception as e:
    print(f"Database connection error: {e}")
    engine = None
    Session = None
