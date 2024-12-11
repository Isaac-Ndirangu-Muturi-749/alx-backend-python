import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        """Initialize the context manager with the database name."""
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        """Establish a database connection when entering the context."""
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the database connection when exiting the context."""
        if self.connection:
            self.connection.close()

# Usage of the custom context manager
if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
