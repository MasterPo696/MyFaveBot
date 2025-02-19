from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import streamlit as st
from app.models.user import Base
import os

# Create a database directory if it doesn't exist
if not os.path.exists('database'):
    os.makedirs('database')

# Use SQLite instead of PostgreSQL
DATABASE_URL = "sqlite:///database/app.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=False
)

# Create all tables
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()