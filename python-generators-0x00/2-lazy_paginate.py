seed = __import__('seed')


def paginate_users(page_size, offset):
    """
    Fetch a specific page of data from the database based on page size and offset.

    Args:
        page_size (int): Number of rows per page.
        offset (int): Number of rows to skip.

    Returns:
        list: A list of rows fetched from the database.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """
    A generator function to lazily fetch paginated data from the database.

    Args:
        page_size (int): Number of rows per page.

    Yields:
        list: A list of rows representing a page of data.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
 