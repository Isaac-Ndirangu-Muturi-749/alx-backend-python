Here’s the Python script `seed.py` that satisfies the requirements and a detailed `README.md` explaining the setup, usage, and functionality.

---

### `seed.py`

```python
import mysql.connector
import csv
import uuid

# Function to connect to MySQL server
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Update with your MySQL username
            password="password"  # Update with your MySQL password
        )
        print("Connected to MySQL server.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to create the database ALX_prodev if it doesn't exist
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created or already exists.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

# Function to connect to the ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Update with your MySQL username
            password="password",  # Update with your MySQL password
            database="ALX_prodev"
        )
        print("Connected to ALX_prodev database.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to create the table user_data if it doesn't exist
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3, 0) NOT NULL
            );
        """)
        print("Table user_data created successfully.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

# Function to insert data into the user_data table
def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Generate a UUID for user_id
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']

                # Insert data if it does not already exist
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    email = VALUES(email),
                    age = VALUES(age);
                """, (user_id, name, email, age))
        connection.commit()
        print("Data inserted into user_data table successfully.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    except FileNotFoundError:
        print(f"File {csv_file} not found.")
```

---

### `README.md`

```markdown
# Python Generators: Streaming Rows from SQL Database

This project demonstrates how to set up a MySQL database, create a table, populate it with data from a CSV file, and stream rows using Python.

## Objective
Create a Python generator to stream rows from an SQL database table (`user_data`) one by one.

## Features
- Sets up a MySQL database (`ALX_prodev`) and a table (`user_data`) with the required schema.
- Populates the table with sample data from a CSV file (`user_data.csv`).
- Includes functionality for safe database connection and operation.

## Prerequisites
Ensure the following are installed on your system:
- Python 3.8 or above
- MySQL server
- MySQL Python Connector (`pip install mysql-connector-python`)

## Setup and Usage

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/alx-backend-python.git
cd alx-backend-python/python-generators-0x00
```

### 2. Install Requirements
Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install mysql-connector-python
```

### 3. Prepare MySQL Server
Ensure MySQL is running, and update the following details in `seed.py` if necessary:
- MySQL user: `root`
- MySQL password: `password`

### 4. Run the Script
Run the `0-main.py` script to:
- Create the database and table if they don't exist.
- Populate the table from `user_data.csv`.
- Display the first five rows from the table.

```bash
python3 0-main.py
```

### Example Output
```plaintext
Connected to MySQL server.
Database ALX_prodev created or already exists.
Connected to ALX_prodev database.
Table user_data created successfully.
Data inserted into user_data table successfully.
Database ALX_prodev is present
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67),
('006bfede-724d-4cdd-a2a6-59700f40d0da', 'Glenda Wisozk', 'Miriam21@gmail.com', 119),
('006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'Daniel Fahey IV', 'Delia.Lesch11@hotmail.com', 49),
('00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'Ronnie Bechtelar', 'Sandra19@yahoo.com', 22),
('00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'Alma Bechtelar', 'Shelly_Balistreri22@hotmail.com', 102)]
```

### 5. Adding the Generator (Optional)
To create a generator for streaming rows, add this function to `seed.py`:
```python
def stream_rows(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    for row in cursor:
        yield row
    cursor.close()
```

You can then use the generator as:
```python
for row in stream_rows(connection):
    print(row)
```

## Files
- **seed.py**: Contains the main functionality for database operations.
- **user_data.csv**: Sample data for populating the database.
- **0-main.py**: Script for testing the functionality.
