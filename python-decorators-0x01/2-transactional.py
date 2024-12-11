import sqlite3
import functools

def with_db_connection(func):
    """Decorator to handle opening and closing database connections."""
    @functools.wraps(func)
    def wrapper_with_db_connection(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result

    return wrapper_with_db_connection

def transactional(func):
    """Decorator to manage database transactions."""
    @functools.wraps(func)
    def wrapper_transactional(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit the transaction if successful
            return result
        except Exception as e:
            conn.rollback()  # Rollback the transaction if an error occurs
            raise e

    return wrapper_transactional

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """Update the email of a user in the database."""
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
