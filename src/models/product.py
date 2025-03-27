# src/models/product.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, validates
from src.database.db_connection import Base

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    
    # Foreign key relationship with category
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship('Category', back_populates='products')
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Product name cannot be empty")
        if len(name) > 100:
            raise ValueError("Product name cannot exceed 100 characters")
        return name.strip()
    
    @validates('price')
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        return price
    
    @validates('stock_quantity')
    def validate_stock_quantity(self, key, stock_quantity):
        if stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        return stock_quantity
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', stock={self.stock_quantity})>"