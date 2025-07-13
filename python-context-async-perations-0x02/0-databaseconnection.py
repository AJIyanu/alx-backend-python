import mysql.connector

class DatabaseConnection:
    def __init__(self, config):
        self.config = config
        self.connection = None

    def __enter__(self):
        print("Connecting to database...")
        self.connection = mysql.connector.connect(**self.config)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")

config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}

with DatabaseConnection(config) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        print(row)