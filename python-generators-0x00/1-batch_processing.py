seed = __import__('seed')


def stream_users_in_batches(batch_size):
    """
    A generator function to fetch rows from the user_data table in batches.

    Args:
        batch_size (int): Number of rows to fetch per batch.

    Yields:
        list: A list of user rows from the user_data table.
    """
    connection = seed.connect_to_prodev()
    if not connection:
        raise Exception("Failed to connect to the database.")

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
    except Exception as e:
        print(f"Error fetching data in batches: {e}")
    finally:
        cursor.close()
        connection.close()


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25.

    Args:
        batch_size (int): Number of rows to process per batch.

    Yields:
        dict: Filtered user data with age > 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
