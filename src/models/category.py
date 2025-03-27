# src/models/category.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.db_connection import Base

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    
    # Relationship with products
    products = relationship('Product', back_populates='category', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"

