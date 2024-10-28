import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///users.db')
print(f"DATABASE_URL is: {DATABASE_URL}")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}  if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(bind=engine)
