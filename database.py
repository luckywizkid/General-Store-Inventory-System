import sqlite3

def create_database():

    connection = sqlite3.connect('general_store.db')

    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            min_quantity INTEGER NOT NULL

        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_name TEXT NOT NULL,
            contact_person TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL
        )
    ''')         
    connection.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity_sold INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_amount REAL NOT NULL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')         
    connection.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                rating INTEGER NOT NULL,
                feedback_message TEXT NOT NULL,
                feedback_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
  
    connection.commit()

    connection.close()

    print("Database created successfully!")

def add_sample_products():
    connection = sqlite3.connect('general_store.db')

    products = [
        ("A4 Notebook", "Stationery", 113.00, 20, 5),
        ("A5 Notebook", "Stationery", 25.00, 30, 5),
        ("Exercise Book", "Stationery", 5.70, 50, 10),
        ("Counter Book", "Stationery", 21.50, 20, 5),
        ("Blue Ballpoint Pen", "Stationery", 8.00, 50, 10),
        ("Colour Pencils", "School Supplies", 13.80, 25, 5),
        ("Eraser", "School Supplies", 4.60, 40, 10),
        ("Glue Stick", "School Supplies", 14.70, 20, 5),
        ("School Scissors", "School Supplies", 8.90, 20, 5),
        ("Plastic Book Covers", "School Supplies", 15.20, 25, 5),
        ("Ruler", "School Supplies", 3.50, 40, 10),
        ("Flip File", "Stationery", 15.50, 25, 5),
        ("Clear Tape", "Stationery", 5.50, 30, 5),
        ("Super Glue", "Household", 27.99, 15, 5),
        ("Toilet Rolls (4-pack)", "Household", 32.00, 20, 5),
        ("Liquid Hand Soap", "Household", 25.00, 20, 5),
        ("Wet Wipes", "Household", 48.30, 15, 5),
        ("Tissues", "Household", 16.99, 25, 5),
        ("Gift Bag", "Household", 14.99, 20, 5),
        ("Glue and Craft Supplies", "School Supplies", 24.99, 15, 5)
    ]

    for product in products:
        connection.execute('''
            INSERT INTO products
            (product_name, category, price, quantity, min_quantity)
            SELECT ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM products WHERE product_name = ?
            )
        ''', product + (product[0],))

    connection.commit()
    connection.close()

    print("Sample products added successfully!")


if __name__ == '__main__':
    create_database()
    add_sample_products()