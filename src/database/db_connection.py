# src/database/db_connection.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create base class for declarative models
Base = declarative_base()

class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._setup_connection()
        return cls._instance
    
    def _setup_connection(self):
        try:
            # Use SQLite database with full path
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'inventory.db')
            self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
            self.Session = sessionmaker(bind=self.engine)
        except SQLAlchemyError as e:
            print(f"Database connection error: {e}")
            raise
    
    def get_session(self):
        return self.Session()
    
    def create_tables(self):
        Base.metadata.create_all(self.engine)
    
    def drop_tables(self):
        Base.metadata.drop_all(self.engine)