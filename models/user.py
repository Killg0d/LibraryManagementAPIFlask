import sqlite3
from db.database import get_db_connection

def create_user(username: str, password: str):
    """
    Create a new user with the specified username and password.

    Args:
        username (str): The username of the new user.
        password (str): The password for the new user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )
    conn.commit()
    conn.close()

def get_user_by_id(user_id: int):
    """
    Retrieve a user by their unique ID.

    Args:
        user_id (int): The unique ID of the user.

    Returns:
        tuple: A tuple representing the user record, or None if no user is found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user_password(user_id: int, new_password: str):
    """
    Update the password for a specific user.

    Args:
        user_id (int): The unique ID of the user.
        new_password (str): The new password for the user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password = ? WHERE id = ?",
        (new_password, user_id)
    )
    conn.commit()
    conn.close()

def delete_user(user_id: int):
    """
    Delete a user from the database.

    Args:
        user_id (int): The unique ID of the user to delete.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def authenticate_user(username: str, password: str) -> int:
    """Authenticate a user and return their ID if successful."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user["id"] if user else None