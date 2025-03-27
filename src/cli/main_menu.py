# src/cli/main_menu.py
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
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
            
            choice = Prompt.ask("Enter your choice", choices=['1', '2', '3', '4'])
            
            if choice == '1':
                self.product_menu()
            elif choice == '2':
                self.category_menu()
            elif choice == '3':
                self.display_low_stock_alerts()
            elif choice == '4':
                self.console.print("[bold yellow]Thank you for using Inventory Management System![/bold yellow]")
                sys.exit()
    
    def product_menu(self):
        while True:
            self.console.print(Panel.fit(
                "[bold blue]Product Management[/bold blue]\n" +
                "1. Create Product\n" +
                "2. Delete Product\n" +
                "3. List All Products\n" +
                "4. Find Product\n" +
                "5. Update Stock\n" +
                "6. Back to Main Menu"
            ))
            
            choice = Prompt.ask("Enter your choice", choices=['1', '2', '3', '4', '5', '6'])
            
            try:
                if choice == '1':
                    self.create_product()
                elif choice == '2':
                    self.delete_product()
                elif choice == '3':
                    self.list_all_products()
                elif choice == '4':
                    self.find_product()
                elif choice == '5':
                    self.update_product_stock()
                elif choice == '6':
                    break
            except ValueError as e:
                self.console.print(f"[red]Error: {e}[/red]")
    
    def category_menu(self):
        while True:
            self.console.print(Panel.fit(
                "[bold blue]Category Management[/bold blue]\n" +
                "1. Create Category\n" +
                "2. Delete Category\n" +
                "3. List All Categories\n" +
                "4. Find Category\n" +
                "5. View Category Products\n" +
                "6. Back to Main Menu"
            ))
            
            choice = Prompt.ask("Enter your choice", choices=['1', '2', '3', '4', '5', '6'])
            
            try:
                if choice == '1':
                    self.create_category()
                elif choice == '2':
                    self.delete_category()
                elif choice == '3':
                    self.list_all_categories()
                elif choice == '4':
                    self.find_category()
                elif choice == '5':
                    self.view_category_products()
                elif choice == '6':
                    break
            except ValueError as e:
                self.console.print(f"[red]Error: {e}[/red]")
    
    def create_product(self):
        # List categories first
        categories = self.category_service.get_all_categories()
        if not categories:
            self.console.print("[yellow]No categories exist. Please create a category first.[/yellow]")
            return
        
        # Show category selection
        category_table = Table(title="Available Categories")
        category_table.add_column("ID")
        category_table.add_column("Name")
        for cat in categories:
            category_table.add_row(str(cat.id), cat.name)
        self.console.print(category_table)
        
        # Prompt for product details
        name = Prompt.ask("Enter product name")
        price = Prompt.ask("Enter product price", type=float)
        category_id = Prompt.ask("Enter category ID", type=int)
        description = Prompt.ask("Enter product description (optional)", default="")
        stock = Prompt.ask("Enter initial stock quantity", type=int, default=0)
        
        product = self.product_service.create_product(
            name, price, category_id, description, stock
        )
        self.console.print(f"[green]Product '{product.name}' created successfully![/green]")
    
    def create_category(self):
        name = Prompt.ask("Enter category name")
        description = Prompt.ask("Enter category description (optional)", default="")
        
        category = self.category_service.create_category(name, description)
        self.console.print(f"[green]Category '{category.name}' created successfully![/green]")
    
    def delete_product(self):
        product_id = Prompt.ask("Enter product ID to delete", type=int)
        confirm = Confirm.ask("Are you sure you want to delete this product?")
        
        if confirm:
            self.product_service.delete_product(product_id)
            self.console.print("[green]Product deleted successfully![/green]")
    
    def delete_category(self):
        category_id = Prompt.ask("Enter category ID to delete", type=int)
        confirm = Confirm.ask("Are you sure you want to delete this category?")
        
        if confirm:
            self.category_service.delete_category(category_id)
            self.console.print("[green]Category deleted successfully![/green]")
    
    def list_all_products(self):
        products = self.product_service.get_all_products()
        
        if not products:
            self.console.print("[yellow]No products found.[/yellow]")
            return
        
        product_table = Table(title="Product List")
        product_table.add_column("ID")
        product_table.add_column("Name")
        product_table.add_column("Price")
        product_table.add_column("Stock")
        product_table.add_column("Category")
        
        for product in products:
            product_table.add_row(
                str(product.id), 
                product.name, 
                f"${product.price:.2f}", 
                str(product.stock_quantity),
                product.category.name
            )
        
        self.console.print(product_table)
    
    def list_all_categories(self):
        categories = self.category_service.get_all_categories()
        
        if not categories:
            self.console.print("[yellow]No categories found.[/yellow]")
            return
        
        category_table = Table(title="Category List")
        category_table.add_column("ID")
        category_table.add_column("Name")
        category_table.add_column("Description")
        
        for category in categories:
            category_table.add_row(
                str(category.id), 
                category.name, 
                category.description or "No description"
            )
        
        self.console.print(category_table)
    
    def find_product(self):
        search_type = Prompt.ask("Search by", choices=['id', 'name'])
        
        if search_type == 'id':
            product_id = Prompt.ask("Enter product ID", type=int)
            product = self.product_service.find_product_by_id(product_id)
        else:
            name = Prompt.ask("Enter product name")
            product = self.product_service.find_product_by_name(name)
        
        if product:
            self.console.print(Panel.fit(
                f"[bold]Product Details[/bold]\n"
                f"ID: {product.id}\n"
                f"Name: {product.name}\n"
                f"Price: ${product.price:.2f}\n"
                f"Stock: {product.stock_quantity}\n"
                f"Category: {product.category.name}\n"
                f"Description: {product.description or 'No description'}"
            ))
        else:
            self.console.print("[yellow]Product not found.[/yellow]")
    
    def find_category(self):
        search_type = Prompt.ask("Search by", choices=['id', 'name'])
        
        if search_type == 'id':
            category_id = Prompt.ask("Enter category ID", type=int)
            category = self.category_service.find_category_by_id(category_id)
        else:
            name = Prompt.ask("Enter category name")
            category = self.category_service.find_category_by_name(name)
        
        if category:
            self.console.print(Panel.fit(
                f"[bold]Category Details[/bold]\n"
                f"ID: {category.id}\n"
                f"Name: {category.name}\n"
                f"Description: {category.description or 'No description'}"
            ))
        else:
            self.console.print("[yellow]Category not found.[/yellow]")
    
    def update_product_stock(self):
        product_id = Prompt.ask("Enter product ID", type=int)
        quantity_change = Prompt.ask("Enter stock quantity change (positive to add, negative to remove)", type=int)
        
        updated_product = self.product_service.update_stock(product_id, quantity_change)
        self.console.print(f"[green]Stock updated. New stock: {updated_product.stock_quantity}[/green]")
    
    def view_category_products(self):
        category_id = Prompt.ask("Enter category ID", type=int)
        products = self.product_service.get_products_by_category(category_id)
        
        if not products:
            self.console.print("[yellow]No products found in this category.[/yellow]")
            return
        
        product_table = Table(title=f"Products in Category {category_id}")
        product_table.add_column("ID")
        product_table.add_column("Name")
        product_table.add_column("Price")
        product_table.add_column("Stock")
        
        for product in products:
            product_table.add_row(
                str(product.id), 
                product.name, 
                f"${product.price:.2f}", 
                str(product.stock_quantity)
            )
        
        self.console.print(product_table)
    
    def display_low_stock_alerts(self):
        low_stock_products = self.product_service.get_low_stock_products()
        
        if low_stock_products:
            low_stock_table = Table(title="Low Stock Alerts")
            low_stock_table.add_column("ID")
            low_stock_table.add_column("Name")
            low_stock_table.add_column("Current Stock")
            low_stock_table.add_column("Category")
            
            for product in low_stock_products:
                low_stock_table.add_row(
                    str(product.id), 
                    product.name, 
                    str(product.stock_quantity),
                    product.category.name
                )
            
            self.console.print(low_stock_table)
        else:
            self.console.print("[green]No low stock products![/green]")

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