import sqlite3
import functools
import hashlib

query_cache = {}

def with_db_connection(func):
    """Decorator to handle opening and closing of database connections."""
    @functools.wraps(func)
    def wrapper_with_connection(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper_with_connection

def cache_query(func):
    """Decorator to cache the results of database queries based on the SQL query string."""
    @functools.wraps(func)
    def wrapper_with_cache(conn, query, *args, **kwargs):
        query_hash = hashlib.sha256(query.encode()).hexdigest()
        if query_hash in query_cache:
            print("Using cached result for query.")
            return query_cache[query_hash]

        print("Executing query and caching result.")
        result = func(conn, query, *args, **kwargs)
        query_cache[query_hash] = result
        return result
    return wrapper_with_cache

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
