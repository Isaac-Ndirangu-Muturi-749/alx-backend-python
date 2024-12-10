seed = __import__('seed')

def stream_users():
    """
    A generator function to stream rows from the user_data table one by one.
    """
    # Establish connection to the ALX_prodev database using the function from seed.py
    connection = seed.connect_to_prodev()
    if not connection:
        raise Exception("Failed to connect to the database.")

    try:
        # Execute the query and use the generator to yield rows
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row
    except Exception as e:
        print(f"Error fetching data: {e}")
    finally:
        # Ensure cursor and connection are closed
        cursor.close()
        connection.close()
