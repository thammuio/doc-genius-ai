import sqlite3

# Function to lookup truck_id in SQLite database
def lookup_truck_id(truck_id):
    conn = sqlite3.connect('lookups_sqlite.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TruckStatus WHERE truck_id = ?", (truck_id,))
    result = cursor.fetchone()
    conn.close()
    return result


