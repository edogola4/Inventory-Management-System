# src/services/category_service.py
from typing import List, Optional
from src.database.db_connection import DatabaseConnection
from src.models.category import Category
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class CategoryService:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_category(self, name: str, description: Optional[str] = None) -> Category:
        session = self.db.get_session()
        try:
            category = Category(name=name, description=description)
            session.add(category)
            session.commit()
            return category
        except (IntegrityError, ValueError) as e:
            session.rollback()
            raise ValueError(f"Error creating category: {str(e)}")
        finally:
            session.close()
    
    def delete_category(self, category_id: int) -> bool:
        session = self.db.get_session()
        try:
            category = session.query(Category).filter_by(id=category_id).first()
            if not category:
                raise ValueError(f"Category with id {category_id} not found")
            session.delete(category)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Error deleting category: {str(e)}")
        finally:
            session.close()
    
    def get_all_categories(self) -> List[Category]:
        session = self.db.get_session()
        try:
            return session.query(Category).all()
        finally:
            session.close()
    
    def find_category_by_id(self, category_id: int) -> Optional[Category]:
        session = self.db.get_session()
        try:
            return session.query(Category).filter_by(id=category_id).first()
        finally:
            session.close()
    
    def find_category_by_name(self, name: str) -> Optional[Category]:
        session = self.db.get_session()
        try:
            return session.query(Category).filter_by(name=name).first()
        finally:
            session.close()

