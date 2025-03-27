# src/database/db_connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

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
            # Use SQLite database in the project root
            self.engine = create_engine('sqlite:///inventory.db', echo=False)
            self.Session = sessionmaker(bind=self.engine)
        except SQLAlchemyError as e:
            print(f"Database connection error: {e}")
            raise
    
    def get_session(self):
        return self.Session()
    
    def create_tables(self):
        Base.metadata.create_all(self.engine)