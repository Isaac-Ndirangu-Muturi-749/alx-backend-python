seed = __import__('seed')

def stream_user_ages():
    """
    Generator function to yield user ages one by one from the database.

    Yields:
        int: The age of each user in the database.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']
    connection.close()

def calculate_average_age():
    """
    Calculates the average age of users using the `stream_user_ages` generator.

    Prints:
        str: The average age of users.
    """
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found in the dataset.")
    else:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")

if __name__ == "__main__":
    calculate_average_age()
