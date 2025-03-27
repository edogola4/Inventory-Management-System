# src/utils/exceptions.py
class InventoryError(Exception):
    """Base class for Inventory Management Exceptions"""
    def __init__(self, message: str, error_code: str = "UNKNOWN_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class ValidationError(InventoryError):
    """Raised when input validation fails"""
    def __init__(self, message: str):
        super().__init__(message, error_code="VALIDATION_ERROR")

class DatabaseError(InventoryError):
    """Raised for database-related errors"""
    def __init__(self, message: str):
        super().__init__(message, error_code="DATABASE_ERROR")

class ResourceNotFoundError(InventoryError):
    """Raised when a requested resource is not found"""
    def __init__(self, resource_type: str, identifier: any):
        message = f"{resource_type.capitalize()} with identifier {identifier} not found"
        super().__init__(message, error_code="RESOURCE_NOT_FOUND")

# Example usage in services
class ProductService:
    def find_product_by_id(self, product_id: int) -> Product: # type: ignore
        session = self.db.get_session()
        try:
            product = session.query(Product).filter_by(id=product_id).first() # type: ignore
            if not product:
                raise ResourceNotFoundError("product", product_id)
            return product
        except SQLAlchemyError as e: # type: ignore
            raise DatabaseError(f"Database error: {str(e)}")
        finally:
            session.close()