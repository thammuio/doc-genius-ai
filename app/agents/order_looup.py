import sqlite3

# Step 1: Set up SQLite Database and Table
def setup_database():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Step 2: Connect to SQLite Database
def connect_db():
    return sqlite3.connect('orders.db')

# Step 3: Query the Database
def get_order_status(order_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM orders WHERE order_id = ?', (order_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

# Step 4: AI Agent Logic
def check_order_status(order_id):
    status = get_order_status(order_id)
    if status:
        if status.lower() == 'shipped':
            return f"Order {order_id} has been shipped."
        else:
            return f"Order {order_id} has not been shipped. Current status: {status}."
    else:
        return f"Order {order_id} not found."

# Example Usage
if __name__ == "__main__":
    setup_database()
    
    # Insert some example data
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orders (order_id, status) VALUES (?, ?)', (1, 'shipped'))
    cursor.execute('INSERT INTO orders (order_id, status) VALUES (?, ?)', (2, 'processing'))
    conn.commit()
    conn.close()
    
    # Check order status
    print(check_order_status(1))  # Output: Order 1 has been shipped.
    print(check_order_status(2))  # Output: Order 2 has not been shipped. Current status: processing.
    print(check_order_status(3))  # Output: Order 3 not found.