import sqlite3
from sqlite3 import Error

# Function to create a connection to the SQLite database
def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection established to SQLite")
    except Error as e:
        print(e)
    return conn

# Function to create the TruckStatus table
def create_table(conn):
    """ Create a table from the create_table_sql statement """
    try:
        sql_create_table = """CREATE TABLE IF NOT EXISTS TruckStatus (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                truck_id TEXT NOT NULL,
                                status TEXT NOT NULL,
                                route TEXT NOT NULL,
                                driver_notes TEXT,
                                additional_info TEXT,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                            );"""
        cursor = conn.cursor()
        cursor.execute(sql_create_table)
        print("TruckStatus table created")
    except Error as e:
        print(e)

# Function to insert data into the TruckStatus table
def insert_truck_status(conn, truck_id, status, route, driver_notes=None, additional_info=None):
    """ Insert a new row into the TruckStatus table """
    sql_insert = '''INSERT INTO TruckStatus(truck_id, status, route, driver_notes, additional_info)
                    VALUES(?,?,?,?,?)'''
    cursor = conn.cursor()
    cursor.execute(sql_insert, (truck_id, status, route, driver_notes, additional_info))
    conn.commit()
    return cursor.lastrowid

# Function to query all rows in the TruckStatus table
def select_all_truck_status(conn):
    """ Query all rows in the TruckStatus table """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TruckStatus")

    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Main function to use the above functionality
def main():
    database = r"lookups_sqlite.db"

    # Create a database connection
    conn = create_connection(database)

    if conn is not None:
        # Create the TruckStatus table
        create_table(conn)

        # Insert a few records
        insert_truck_status(conn, "LOG-TRK-7563", "In Transit", "Route A", "Encountered heavy traffic near city center, still on schedule", "High-priority delivery with sensitive cargo")

        # Truck 78567 has successfully completed its delivery on Route B. The driver noted that the delivery was completed
        # ahead of time, and the customer was satisfied. The additional info indicates that the truck is now heading back to the depot for routine maintenance.
        insert_truck_status(conn, "LOG-TRK-5436", "Delivered", "Route B", "Delivery completed ahead of time, customer satisfied", "Returning to depot for routine maintenance")

        # Truck 56789 is delayed on Route B due to an unexpected road closure caused by an accident. The driver noted
        # that they have taken a detour, but the new route will add an estimated 2 hours to the delivery time. Additional info mentions that the driver has informed the customer about the delay.
        insert_truck_status(conn, "LOG-TRK-9922", "Delayed", "Route B", "Delayed due to road closure, taking detour with 2 hours additional time", "Customer informed about the delay")
        # Query all records
        print("All truck statuses:")
        select_all_truck_status(conn)

    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()
