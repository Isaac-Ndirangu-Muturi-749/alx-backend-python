import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Establish the database connection and create a cursor
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self

    def execute(self):
        # Execute the provided query with parameters
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        # Ensure the connection is closed properly
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

# Usage example
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("users.db", query, params) as executor:
        results = executor.execute()
        for row in results:
            print(row)
