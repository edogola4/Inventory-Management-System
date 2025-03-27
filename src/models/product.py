# src/models/product.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
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
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', stock={self.stock_quantity})>"