# src/services/product_service.py
from typing import List, Optional
from src.database.db_connection import DatabaseConnection
from src.models.product import Product
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class ProductService:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_product(self, name: str, price: float, category_id: int, 
                       description: Optional[str] = None, 
                       stock_quantity: int = 0) -> Product:
        session = self.db.get_session()
        try:
            product = Product(
                name=name, 
                price=price, 
                category_id=category_id, 
                description=description, 
                stock_quantity=stock_quantity
            )
            session.add(product)
            session.commit()
            return product
        except (IntegrityError, ValueError) as e:
            session.rollback()
            raise ValueError(f"Error creating product: {str(e)}")
        finally:
            session.close()
    
    def delete_product(self, product_id: int) -> bool:
        session = self.db.get_session()
        try:
            product = session.query(Product).filter_by(id=product_id).first()
            if not product:
                raise ValueError(f"Product with id {product_id} not found")
            session.delete(product)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Error deleting product: {str(e)}")
        finally:
            session.close()
    
    def get_all_products(self) -> List[Product]:
        session = self.db.get_session()
        try:
            return session.query(Product).all()
        finally:
            session.close()
    
    def find_product_by_id(self, product_id: int) -> Optional[Product]:
        session = self.db.get_session()
        try:
            return session.query(Product).filter_by(id=product_id).first()
        finally:
            session.close()
    
    def find_product_by_name(self, name: str) -> Optional[Product]:
        session = self.db.get_session()
        try:
            return session.query(Product).filter_by(name=name).first()
        finally:
            session.close()
    
    def get_products_by_category(self, category_id: int) -> List[Product]:
        session = self.db.get_session()
        try:
            return session.query(Product).filter_by(category_id=category_id).all()
        finally:
            session.close()
    
    def update_stock(self, product_id: int, quantity_change: int) -> Product:
        session = self.db.get_session()
        try:
            product = session.query(Product).filter_by(id=product_id).first()
            if not product:
                raise ValueError(f"Product with id {product_id} not found")
            
            new_stock = product.stock_quantity + quantity_change
            if new_stock < 0:
                raise ValueError("Stock cannot be negative")
            
            product.stock_quantity = new_stock
            session.commit()
            return product
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Error updating stock: {str(e)}")
        finally:
            session.close()
    
    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        session = self.db.get_session()
        try:
            return session.query(Product).filter(Product.stock_quantity <= threshold).all()
        finally:
            session.close()