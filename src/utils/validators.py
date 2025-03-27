# src/utils/validators.py
import re
from typing import Any, Optional

class InputValidator:
    @staticmethod
    def validate_name(name: str, min_length: int = 2, max_length: int = 100) -> str:
        """
        Validate name with comprehensive checks
        """
        if not name:
            raise ValueError("Name cannot be empty")
        
        # Remove leading/trailing whitespaces
        name = name.strip()
        
        # Check length
        if len(name) < min_length:
            raise ValueError(f"Name must be at least {min_length} characters long")
        
        if len(name) > max_length:
            raise ValueError(f"Name cannot exceed {max_length} characters")
        
        # Check for valid characters (letters, spaces, hyphens)
        if not re.match(r'^[A-Za-z\s\-]+$', name):
            raise ValueError("Name can only contain letters, spaces, and hyphens")
        
        return name
    
    @staticmethod
    def validate_price(price: float, min_price: float = 0, max_price: float = 100000) -> float:
        """
        Validate price with comprehensive checks
        """
        try:
            price = float(price)
        except (ValueError, TypeError):
            raise ValueError("Price must be a valid number")
        
        if price < min_price:
            raise ValueError(f"Price cannot be negative. Minimum price is {min_price}")
        
        if price > max_price:
            raise ValueError(f"Price is too high. Maximum price is {max_price}")
        
        # Round to 2 decimal places
        return round(price, 2)
    
    @staticmethod
    def validate_stock_quantity(quantity: int, min_quantity: int = 0, max_quantity: int = 10000) -> int:
        """
        Validate stock quantity with comprehensive checks
        """
        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            raise ValueError("Stock quantity must be a valid integer")
        
        if quantity < min_quantity:
            raise ValueError(f"Stock quantity cannot be negative. Minimum is {min_quantity}")
        
        if quantity > max_quantity:
            raise ValueError(f"Stock quantity too high. Maximum is {max_quantity}")
        
        return quantity
    
    @staticmethod
    def validate_description(description: Optional[str], max_length: int = 255) -> Optional[str]:
        """
        Validate optional description
        """
        if description is None:
            return None
        
        description = description.strip()
        
        if len(description) > max_length:
            raise ValueError(f"Description cannot exceed {max_length} characters")
        
        return description or None