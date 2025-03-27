# src/cli/main_menu.py
import sys
from rich.console import Console
from rich.panel import Panel
from rich.menu import Menu # type: ignore
from src.services.category_service import CategoryService
from src.services.product_service import ProductService

class InventoryManagementCLI:
    def __init__(self):
        self.console = Console()
        self.category_service = CategoryService()
        self.product_service = ProductService()
    
    def display_main_menu(self):
        while True:
            self.console.print(Panel.fit(
                "[bold green]Inventory Management System[/bold green]\n" +
                "1. Product Management\n" +
                "2. Category Management\n" +
                "3. Low Stock Alerts\n" +
                "4. Exit"
            ))
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == '1':
                self.product_menu()
            elif choice == '2':
                self.category_menu()
            elif choice == '3':
                self.display_low_stock_alerts()
            elif choice == '4':
                sys.exit()
            else:
                self.console.print("[red]Invalid choice. Please try again.[/red]")
    
    def product_menu(self):
        # Similar implementation with product management options
        pass
    
    def category_menu(self):
        # Similar implementation with category management options
        pass
    
    def display_low_stock_alerts(self):
        low_stock_products = self.product_service.get_low_stock_products()
        if low_stock_products:
            self.console.print(Panel.fit(
                "[bold yellow]Low Stock Alerts[/bold yellow]\n" +
                "\n".join([f"{p.name}: {p.stock_quantity} units" for p in low_stock_products])
            ))
        else:
            self.console.print("[green]No low stock products![/green]")

