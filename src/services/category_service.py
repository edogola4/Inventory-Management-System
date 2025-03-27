# src/services/category_service.py
from src.database.db_connection import DatabaseConnection
from src.models.category import Category
from sqlalchemy.exc import IntegrityError

class CategoryService:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_category(self, name, description=None):
        session = self.db.get_session()
        try:
            category = Category(name=name, description=description)
            session.add(category)
            session.commit()
            return category
        except IntegrityError:
            session.rollback()
            raise ValueError(f"Category '{name}' already exists")
        finally:
            session.close()
    
    def get_all_categories(self):
        session = self.db.get_session()
        try:
            return session.query(Category).all()
        finally:
            session.close()

