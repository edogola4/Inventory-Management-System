# src/services/product_service.py
from src.database.db_connection import DatabaseConnection
from src.models.product import Product
from sqlalchemy.exc import IntegrityError

class ProductService:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_product(self, name, price, category_id, description=None, stock_quantity=0):
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
        except IntegrityError:
            session.rollback()
            raise ValueError(f"Unable to create product '{name}'")
        finally:
            session.close()
    
    def get_low_stock_products(self, threshold=10):
        session = self.db.get_session()
        try:
            return session.query(Product).filter(Product.stock_quantity <= threshold).all()
        finally:
            session.close()