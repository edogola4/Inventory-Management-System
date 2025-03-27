# src/models/category.py
from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import relationship, validates
from src.database.db_connection import Base

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    
    # Relationship with products
    products = relationship('Product', back_populates='category', cascade='all, delete-orphan')
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Category name cannot be empty")
        if len(name) > 100:
            raise ValueError("Category name cannot exceed 100 characters")
        return name.strip()
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
