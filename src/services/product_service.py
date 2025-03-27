# src/services/product_service.py

from typing import List, Optional, Dict, Any
from src.database.db_connection import DatabaseConnection
from src.models.product import Product
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import or_, and_

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


class AdvancedProductSearch:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def search_products(self, 
                        name: Optional[str] = None, 
                        min_price: Optional[float] = None, 
                        max_price: Optional[float] = None,
                        category_id: Optional[int] = None,
                        min_stock: Optional[int] = None,
                        max_stock: Optional[int] = None) -> List[Product]:
        """
        Advanced product search with multiple filter options.
        """
        session = self.db.get_session()
        try:
            query = session.query(Product)
            
            # Name search (case-insensitive, partial match)
            if name:
                query = query.filter(Product.name.ilike(f'%{name}%'))
            
            # Price range filter
            if min_price is not None:
                query = query.filter(Product.price >= min_price)
            if max_price is not None:
                query = query.filter(Product.price <= max_price)
            
            # Category filter
            if category_id is not None:
                query = query.filter(Product.category_id == category_id)
            
            # Stock range filter
            if min_stock is not None:
                query = query.filter(Product.stock_quantity >= min_stock)
            if max_stock is not None:
                query = query.filter(Product.stock_quantity <= max_stock)
            
            return query.all()
        finally:
            session.close()
    
    def advanced_product_filter(self, filters: Dict[str, Any]) -> List[Product]:
        """
        Flexible product filtering based on multiple criteria.
        """
        session = self.db.get_session()
        try:
            query = session.query(Product)
            
            # Dynamic filtering based on provided criteria
            for key, value in filters.items():
                if hasattr(Product, key):
                    # Exact match for most fields
                    query = query.filter(getattr(Product, key) == value)
            
            return query.all()
        finally:
            session.close()
    
    def get_products_low_in_stock(self, threshold: int = 10, limit: int = 20) -> List[Product]:
        """
        Get products with stock below a certain threshold.
        """
        session = self.db.get_session()
        try:
            return (session.query(Product)
                    .filter(Product.stock_quantity <= threshold)
                    .order_by(Product.stock_quantity.asc())
                    .limit(limit)
                    .all())
        finally:
            session.close()
