# app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from src.services.product_service import ProductService, AdvancedProductSearch
from src.services.category_service import CategoryService

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # needed for flash messages

# Initialize services
product_service = ProductService()
category_service = CategoryService()
advanced_search = AdvancedProductSearch()

# Home page: a dashboard with links to different operations
@app.route('/')
def index():
    return render_template('index.html')

# Display all products
@app.route('/products')
def list_products():
    try:
        products = product_service.get_all_products()
        return render_template('products.html', products=products)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('index'))

# Form for creating a new product
@app.route('/products/new', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
        try:
            name = request.form['name']
            price = float(request.form['price'])
            category_id = int(request.form['category_id'])
            description = request.form.get('description', '')
            stock_quantity = int(request.form.get('stock_quantity', 0))
            product_service.create_product(name, price, category_id, description, stock_quantity)
            flash("Product created successfully!", "success")
            return redirect(url_for('list_products'))
        except Exception as e:
            flash(f"Error creating product: {e}", "danger")
            return redirect(url_for('new_product'))
    else:
        # Get categories for selection
        categories = category_service.get_all_categories()
        return render_template('new_product.html', categories=categories)

# Display all categories
@app.route('/categories')
def list_categories():
    try:
        categories = category_service.get_all_categories()
        return render_template('categories.html', categories=categories)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('index'))

# Form for creating a new category
@app.route('/categories/new', methods=['GET', 'POST'])
def new_category():
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form.get('description', '')
            category_service.create_category(name, description)
            flash("Category created successfully!", "success")
            return redirect(url_for('list_categories'))
        except Exception as e:
            flash(f"Error creating category: {e}", "danger")
            return redirect(url_for('new_category'))
    else:
        return render_template('new_category.html')

# API endpoint for advanced product search
@app.route('/api/products/search', methods=['GET'])
def search_products():
    name = request.args.get('name')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    category_id = request.args.get('category_id', type=int)
    min_stock = request.args.get('min_stock', type=int)
    max_stock = request.args.get('max_stock', type=int)
    
    try:
        products = advanced_search.search_products(
            name=name,
            min_price=min_price,
            max_price=max_price,
            category_id=category_id,
            min_stock=min_stock,
            max_stock=max_stock
        )
        # Convert products to dicts assuming your Product model has a to_dict() method
        products_list = [product.to_dict() for product in products]
        return jsonify({'status': 'success', 'data': products_list})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
