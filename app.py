from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3


app = Flask(__name__)
app.secret_key = 'general_store_secret_key_2026'
def get_db_connection():
    connection = sqlite3.connect('general_store.db')
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/products')
def products():
    connection = get_db_connection()

    all_products = connection.execute(
        'SELECT * FROM products'
    ).fetchall()

    connection.close()

    return render_template('products.html', products=all_products)

@app.route('/suppliers')
def suppliers():

    connection = get_db_connection()

    all_suppliers = connection.execute(
        'SELECT * FROM suppliers'
    ).fetchall()

    connection.close()

    return render_template('suppliers.html', suppliers=all_suppliers)

@app.route('/edit_supplier/<int:supplier_id>', methods=['GET', 'POST'])
def edit_supplier(supplier_id):

    connection = get_db_connection()

    if request.method == 'POST':

        supplier_name = request.form['supplier_name']
        contact_person = request.form['contact_person']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        connection.execute('''
            UPDATE suppliers
            SET supplier_name = ?,
                contact_person = ?,
                phone = ?,
                email = ?,
                address = ?
            WHERE supplier_id = ?
        ''', (supplier_name, contact_person, phone, email, address, supplier_id))

        connection.commit()
        connection.close()

        return redirect(url_for('suppliers'))

    supplier = connection.execute(
        'SELECT * FROM suppliers WHERE supplier_id = ?',
        (supplier_id,)
    ).fetchone()

    connection.close()

    if supplier is None:
        return "Supplier not found", 404

    return render_template('edit_supplier.html', supplier=supplier)

@app.route('/add_supplier', methods=['POST'])
def add_supplier():

    supplier_name = request.form['supplier_name']
    contact_person = request.form['contact_person']
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']

    connection = get_db_connection()

    connection.execute('''
        INSERT INTO suppliers
        (supplier_name, contact_person, phone, email, address)
        VALUES (?, ?, ?, ?, ?)
    ''', (supplier_name, contact_person, phone, email, address))

    connection.commit()
    connection.close()

    return redirect(url_for('suppliers'))

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):

    connection = get_db_connection()

    connection.execute(
        'DELETE FROM products WHERE product_id = ?',
        (product_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for('products'))

@app.route('/add_product', methods=['POST'])
def add_product():

    product_name = request.form['product_name']
    category = request.form['category']
    price = request.form['price']
    quantity = request.form['quantity']
    min_quantity = request.form['min_quantity']

    connection = get_db_connection()

    connection.execute('''
        INSERT INTO products
        (product_name, category, price, quantity, min_quantity)
        VALUES (?, ?, ?, ?, ?)
    ''', (product_name, category, price, quantity, min_quantity))

    connection.commit()
    connection.close()

    return redirect(url_for('products'))

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):

    connection = get_db_connection()

    if request.method == 'POST':

        product_name = request.form['product_name']
        category = request.form['category']
        price = request.form['price']
        quantity = request.form['quantity']
        min_quantity = request.form['min_quantity']

        connection.execute('''
            UPDATE products
            SET product_name = ?,
                category = ?,
                price = ?,
                quantity = ?,
                min_quantity = ?
            WHERE product_id = ?
        ''', (product_name, category, price, quantity, min_quantity, product_id))

        connection.commit()
        connection.close()

        return redirect(url_for('products'))

    product = connection.execute(
        'SELECT * FROM products WHERE product_id = ?',
        (product_id,)
    ).fetchone()

    connection.close()

    if product is None:
        return "Product not found", 404

    return render_template('edit_product.html', product=product)

@app.route('/')
def dashboard():
    connection = get_db_connection()

    # Total products
    total_products = connection.execute(
        'SELECT COUNT(*) FROM products'
    ).fetchone()[0]

    # Total suppliers
    total_suppliers = connection.execute(
        'SELECT COUNT(*) FROM suppliers'
    ).fetchone()[0]

    # Total sales revenue
    total_sales = connection.execute(
        'SELECT COALESCE(SUM(total_amount), 0) FROM sales'
    ).fetchone()[0]

    # Low stock products
    low_stock = connection.execute(
        'SELECT COUNT(*) FROM products WHERE quantity <= min_quantity'
    ).fetchone()[0]

    # Total customer feedback
    total_feedback = connection.execute(
        'SELECT COUNT(*) FROM feedback'
    ).fetchone()[0]

    # Recent five sales
    recent_sales = connection.execute('''
        SELECT sales.*, products.product_name
        FROM sales
        JOIN products ON sales.product_id = products.product_id
        ORDER BY sales.sale_id DESC
        LIMIT 5
    ''').fetchall()

    # Inventory overview
    inventory_overview = connection.execute('''
        SELECT product_name, quantity, min_quantity
        FROM products
        ORDER BY quantity ASC
        LIMIT 5
    ''').fetchall()

    connection.close()

    return render_template(
        'dashboard.html',
        total_products=total_products,
        total_suppliers=total_suppliers,
        total_sales=total_sales,
        low_stock=low_stock,
        total_feedback=total_feedback,
        recent_sales=recent_sales,
        inventory_overview=inventory_overview
    )

    connection = get_db_connection()

    products = connection.execute(
        'SELECT * FROM products'
    ).fetchall()

    total_products = len(products)

    low_stock = connection.execute(
        'SELECT * FROM products WHERE quantity <= min_quantity'
    ).fetchall()

    connection.close()

    return render_template(
        'dashboard.html',
        total_products=total_products,
        low_stock=len(low_stock)
    )

@app.route('/delete_supplier/<int:supplier_id>', methods=['POST'])
def delete_supplier(supplier_id):
    connection = get_db_connection()
    connection.execute(
        'DELETE FROM suppliers WHERE supplier_id = ?',
        (supplier_id,)
    )
    connection.commit()
    connection.close()
    return redirect(url_for('suppliers'))
@app.route('/sales')
def sales():
    connection = get_db_connection()

    products = connection.execute(
        'SELECT * FROM products'
    ).fetchall()

    all_sales = connection.execute('''
        SELECT sales.*, products.product_name
        FROM sales
        JOIN products ON sales.product_id = products.product_id
        ORDER BY sales.sale_id DESC
    ''').fetchall()

    connection.close()

    return render_template(
        'sales.html',
        products=products,
        sales=all_sales
    )

@app.route('/add_sale', methods=['POST'])
def add_sale():
    product_id = int(request.form['product_id'])
    quantity_sold = int(request.form['quantity_sold'])

    connection = get_db_connection()

    product = connection.execute(
        'SELECT * FROM products WHERE product_id = ?',
        (product_id,)
    ).fetchone()

    if product is None or quantity_sold <= 0:
        connection.close()
        flash("Please select a valid product and quantity.", "error")
        return redirect(url_for('sales'))

    unit_price = product['price']
    total_amount = unit_price * quantity_sold

    if quantity_sold > product['quantity']:
        connection.close()
        flash("Not enough stock available for this sale.", "error")
        return redirect(url_for('sales'))

    connection.execute('''
        UPDATE products
        SET quantity = quantity - ?
        WHERE product_id = ?
    ''', (quantity_sold, product_id))

    connection.execute('''
        INSERT INTO sales
        (product_id, quantity_sold, unit_price, total_amount)
        VALUES (?, ?, ?, ?)
    ''', (product_id, quantity_sold, unit_price, total_amount))

    connection.commit()
    connection.close()

    flash("Sale recorded successfully!", "success")
    return redirect(url_for('sales'))

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


@app.route('/add_feedback', methods=['POST'])
def add_feedback():
    customer_name = request.form.get('customer_name', '').strip()
    rating = int(request.form['rating'])
    feedback_message = request.form['feedback_message'].strip()

    if rating < 1 or rating > 5 or not feedback_message:
        flash("Please provide a valid rating and feedback message.")
        return redirect(url_for('feedback'))

    connection = get_db_connection()
    connection.execute('''
        INSERT INTO feedback (customer_name, rating, feedback_message)
        VALUES (?, ?, ?)
    ''', (customer_name, rating, feedback_message))

    connection.commit()
    connection.close()

    flash("Thank you! Your feedback has been submitted successfully.")
    return redirect(url_for('feedback'))

@app.route('/manage_feedback')
def manage_feedback():
    connection = get_db_connection()

    all_feedback = connection.execute('''
        SELECT * FROM feedback
        ORDER BY feedback_id DESC
    ''').fetchall()

    connection.close()

    return render_template(
        'manage_feedback.html',
        feedback=all_feedback
    )

@app.route('/reports')
def reports():
    connection = get_db_connection()

    # Today's sales revenue
    daily_revenue = connection.execute('''
        SELECT COALESCE(SUM(total_amount), 0)
        FROM sales
        WHERE DATE(sale_date) = DATE('now', 'localtime')
    ''').fetchone()[0]

    # Sales revenue for the last 7 days
    weekly_revenue = connection.execute('''
        SELECT COALESCE(SUM(total_amount), 0)
        FROM sales
        WHERE DATE(sale_date) >= DATE('now', 'localtime', '-6 days')
          AND DATE(sale_date) <= DATE('now', 'localtime')
    ''').fetchone()[0]

    # Total quantity of items sold
    total_items_sold = connection.execute('''
        SELECT COALESCE(SUM(quantity_sold), 0)
        FROM sales
    ''').fetchone()[0]

    # Sales transaction history
    all_sales = connection.execute('''
        SELECT sales.*, products.product_name
        FROM sales
        JOIN products ON sales.product_id = products.product_id
        ORDER BY sales.sale_id DESC
    ''').fetchall()

    connection.close()

    return render_template(
        'reports.html',
        daily_revenue=daily_revenue,
        weekly_revenue=weekly_revenue,
        total_items_sold=total_items_sold,
        sales=all_sales
    )

@app.route('/inventory')
def inventory():
    connection = get_db_connection()

    # Total products
    total_products = connection.execute(
        'SELECT COUNT(*) FROM products'
    ).fetchone()[0]

    # Products currently in stock
    products_in_stock = connection.execute('''
        SELECT COUNT(*) FROM products
        WHERE quantity > min_quantity
    ''').fetchone()[0]

    # Products with low stock
    low_stock = connection.execute('''
        SELECT COUNT(*) FROM products
        WHERE quantity <= min_quantity
    ''').fetchone()[0]

    # All products and their stock status
    all_products = connection.execute('''
        SELECT *,
        CASE
            WHEN quantity <= min_quantity THEN 'Low Stock'
            ELSE 'In Stock'
        END AS stock_status
        FROM products
        ORDER BY product_name
    ''').fetchall()

    connection.close()

    return render_template(
        'inventory.html',
        products=all_products,
        total_products=total_products,
        products_in_stock=products_in_stock,
        low_stock=low_stock
    )

@app.route('/restock/<int:product_id>', methods=['POST'])
def restock(product_id):
    quantity_to_add = int(request.form['quantity_to_add'])

    if quantity_to_add <= 0:
        flash("Please enter a valid restock quantity.")
        return redirect(url_for('inventory'))

    connection = get_db_connection()

    connection.execute('''
        UPDATE products
        SET quantity = quantity + ?
        WHERE product_id = ?
    ''', (quantity_to_add, product_id))

    connection.commit()
    recent_sales = connection.execute('''
        SELECT sales.*, products.product_name
        FROM sales
        JOIN products ON sales.product_id = products.product_id
        ORDER BY sales.sale_id DESC
        LIMIT 5
    ''').fetchall()

    inventory_overview = connection.execute('''
        SELECT product_name, quantity, min_quantity
        FROM products
        ORDER BY quantity ASC
        LIMIT 5
    ''').fetchall()
    connection.close()

    flash("Stock successfully updated!")
    return redirect(url_for('inventory'))

if __name__ == '__main__': 
    app.run(debug=True)