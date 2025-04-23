from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()

# Database URL
DATABASE_URL = "mysql+pymysql://sredbtooluser:<passwordforyourDB>@localhost:3306/sredb"

# Create the SQLAlchemy engine for connecting to the MySQL database
engine = create_engine(DATABASE_URL, echo=True)  # Set echo=True to log SQL queries

# Create a sessionmaker that will generate session objects for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class for model classes to inherit from
Base = declarative_base()

# Function to get the database session (useful in app setups like FastAPI or Flask)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# If you want to create all tables at the start (optional)
#def create_all_tables():
#    Base.metadata.create_all(bind=engine)
#    print("All tables created!")
#
# Example usage of creating tables (you can call this in your main or app startup)
#if __name__ == "__main__":
#    create_all_tables()
##
