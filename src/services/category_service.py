# src/services/category_service.py
from typing import List, Optional
from src.database.db_connection import DatabaseConnection
from src.models.category import Category
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

class CategoryService:
    def __init__(self):
        self.db = DatabaseConnection()
        self.session: Session = self.db.get_session()

    def create_category(self, name: str, description: Optional[str] = None) -> Category:
        try:
            category = Category(name=name, description=description)
            self.session.add(category)
            self.session.commit()
            return category
        except (IntegrityError, ValueError) as e:
            self.session.rollback()
            raise ValueError(f"Error creating category: {str(e)}")

    def delete_category(self, category_id: int) -> bool:
        try:
            category = self.session.query(Category).filter_by(id=category_id).first()
            if not category:
                raise ValueError(f"Category with id {category_id} not found")
            self.session.delete(category)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Error deleting category: {str(e)}")

    def get_all_categories(self) -> List[Category]:
        return self.session.query(Category).all()

    def find_category_by_id(self, category_id: int) -> Optional[Category]:
        return self.session.query(Category).filter_by(id=category_id).first()

    def find_category_by_name(self, name: str) -> Optional[Category]:
        return self.session.query(Category).filter_by(name=name).first()

    def __del__(self):
        if hasattr(self, 'session'):
            self.session.close()