# run.py
from src.database.db_connection import DatabaseConnection
from src.cli.main_menu import InventoryManagementCLI

def main():
    # Initialize database
    db = DatabaseConnection()
    db.create_tables()
    
    # Start CLI
    cli = InventoryManagementCLI()
    cli.display_main_menu()

if __name__ == "__main__":
    main()