"""
Database setup script to create SQLite database with sample data.
Creates a sales database with customers, products, orders, and order_items tables.
"""
import sqlite3
import random
from datetime import datetime, timedelta

# Sample data
CUSTOMER_NAMES = [
    "John Smith", "Sarah Johnson", "Michael Brown", "Emily Davis", "David Wilson",
    "Jessica Martinez", "Christopher Anderson", "Amanda Taylor", "Matthew Thomas",
    "Ashley Jackson", "James White", "Melissa Harris", "Robert Martin", "Nicole Thompson",
    "William Garcia", "Michelle Martinez", "Richard Robinson", "Laura Clark",
    "Joseph Rodriguez", "Kimberly Lewis", "Daniel Lee", "Amy Walker", "Mark Hall",
    "Angela Allen", "Paul Young", "Stephanie King", "Steven Wright", "Rebecca Lopez",
    "Andrew Hill", "Deborah Scott", "Brian Green", "Sharon Adams", "Kevin Baker",
    "Cynthia Gonzalez", "George Nelson", "Kathleen Carter", "Edward Mitchell",
    "Sandra Perez", "Ronald Roberts", "Donna Turner", "Timothy Phillips",
    "Carol Campbell", "Jason Parker", "Nancy Evans", "Jeffrey Edwards",
    "Betty Collins", "Ryan Stewart", "Margaret Sanchez", "Jacob Morris",
    "Dorothy Rogers", "Gary Reed", "Lisa Cook", "Nicholas Morgan", "Helen Bell",
    "Eric Murphy", "Anna Bailey", "Jonathan Rivera", "Brenda Cooper",
    "Larry Richardson", "Pamela Cox", "Scott Howard", "Emma Ward", "Frank Torres",
    "Rachel Peterson", "Raymond Gray", "Carolyn Ramirez", "Alexander James",
    "Janet Watson", "Patrick Brooks", "Maria Kelly", "Jack Sanders", "Frances Price",
    "Dennis Bennett", "Gloria Wood", "Jerry Barnes", "Shirley Ross", "Tyler Henderson",
    "Martha Coleman", "Aaron Jenkins", "Diane Perry", "Jose Powell", "Virginia Long",
    "Peter Patterson", "Marie Hughes", "Harold Flores", "Evelyn Washington", "Carl Butler",
    "Jean Simmons", "Ralph Foster", "Cheryl Gonzales", "Eugene Bryant", "Mildred Alexander",
    "Wayne Russell", "Katherine Griffin", "Louis Diaz", "Lois Hayes", "Philip Myers",
    "Ruby Ford", "Bobby Hamilton", "Norma Graham", "Johnny Sullivan", "Theresa Wallace",
    "Terry Woods", "Judy Cole", "Randy West", "Janice Jordan", "Sean Owens",
    "Marilyn Reynolds", "Ruth Fisher", "Gerald Ellis", "Kathy Harrison", "Albert Gibson"
]

PRODUCTS = [
    {"name": "Laptop Pro 15", "category": "Electronics", "price": 1299.99},
    {"name": "Wireless Mouse", "category": "Electronics", "price": 29.99},
    {"name": "Mechanical Keyboard", "category": "Electronics", "price": 149.99},
    {"name": "4K Monitor 27\"", "category": "Electronics", "price": 399.99},
    {"name": "USB-C Hub", "category": "Electronics", "price": 49.99},
    {"name": "Office Chair", "category": "Furniture", "price": 299.99},
    {"name": "Standing Desk", "category": "Furniture", "price": 599.99},
    {"name": "Desk Lamp", "category": "Furniture", "price": 79.99},
    {"name": "File Cabinet", "category": "Furniture", "price": 199.99},
    {"name": "Bookshelf", "category": "Furniture", "price": 149.99},
    {"name": "Notebook Set", "category": "Office Supplies", "price": 19.99},
    {"name": "Pen Set Premium", "category": "Office Supplies", "price": 34.99},
    {"name": "Stapler", "category": "Office Supplies", "price": 24.99},
    {"name": "Paper Clips Box", "category": "Office Supplies", "price": 9.99},
    {"name": "Binder Set", "category": "Office Supplies", "price": 29.99},
    {"name": "Coffee Maker", "category": "Appliances", "price": 89.99},
    {"name": "Water Bottle", "category": "Appliances", "price": 24.99},
    {"name": "Desk Organizer", "category": "Office Supplies", "price": 39.99},
    {"name": "Whiteboard", "category": "Office Supplies", "price": 59.99},
    {"name": "Printer Paper", "category": "Office Supplies", "price": 14.99},
]

CITIES = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
          "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
          "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis",
          "Seattle", "Denver", "Washington"]

def create_database():
    """Create database and tables."""
    conn = sqlite3.connect('sales_data.db')
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            city TEXT,
            registration_date DATE
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            order_date DATE,
            total_amount REAL,
            status TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    ''')
    
    # Create order_items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price REAL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    ''')
    
    conn.commit()
    return conn, cursor

def populate_database(cursor, conn):
    """Populate database with sample data."""
    # Insert customers (100 customers)
    customers = []
    base_date = datetime(2020, 1, 1)
    for i, name in enumerate(CUSTOMER_NAMES):
        email = f"{name.lower().replace(' ', '.')}@email.com"
        city = random.choice(CITIES)
        reg_date = base_date + timedelta(days=random.randint(0, 1400))
        customers.append((name, email, city, reg_date.strftime('%Y-%m-%d')))
    
    cursor.executemany('''
        INSERT INTO customers (name, email, city, registration_date)
        VALUES (?, ?, ?, ?)
    ''', customers)
    
    # Insert products
    products = [(p['name'], p['category'], p['price']) for p in PRODUCTS]
    cursor.executemany('''
        INSERT INTO products (name, category, price)
        VALUES (?, ?, ?)
    ''', products)
    
    conn.commit()
    
    # Get customer and product IDs
    cursor.execute('SELECT customer_id FROM customers')
    customer_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute('SELECT product_id, price FROM products')
    products_data = cursor.fetchall()
    
    # Create orders (600+ orders to ensure 500+ entities)
    orders = []
    order_items = []
    order_date = datetime(2022, 1, 1)
    
    for order_num in range(600):
        customer_id = random.choice(customer_ids)
        order_dt = order_date + timedelta(days=random.randint(0, 700))
        status = random.choice(['completed', 'pending', 'shipped', 'cancelled'])
        
        # Create order with 1-5 items
        num_items = random.randint(1, 5)
        order_total = 0
        
        for _ in range(num_items):
            product_id, base_price = random.choice(products_data)
            quantity = random.randint(1, 3)
            unit_price = base_price * (1 - random.uniform(0, 0.15))  # Some discount variation
            order_total += unit_price * quantity
            
            order_items.append((order_num + 1, product_id, quantity, round(unit_price, 2)))
        
        orders.append((customer_id, order_dt.strftime('%Y-%m-%d'), round(order_total, 2), status))
    
    cursor.executemany('''
        INSERT INTO orders (customer_id, order_date, total_amount, status)
        VALUES (?, ?, ?, ?)
    ''', orders)
    
    cursor.executemany('''
        INSERT INTO order_items (order_id, product_id, quantity, unit_price)
        VALUES (?, ?, ?, ?)
    ''', order_items)
    
    conn.commit()
    print(f"Database created successfully!")
    print(f"- Customers: {len(customers)}")
    print(f"- Products: {len(products)}")
    print(f"- Orders: {len(orders)}")
    print(f"- Order Items: {len(order_items)}")

if __name__ == "__main__":
    conn, cursor = create_database()
    populate_database(cursor, conn)
    conn.close()

