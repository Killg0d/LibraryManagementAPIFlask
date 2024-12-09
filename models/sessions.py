import time
from db.database import get_db_connection

SESSION_TIMEOUT = 3600  # Session expiration time in seconds (e.g., 1 hour)

def create_session(user_id: int, token: str):
    """
    Create a session for a user and store it in the database.

    Args:
        user_id (int): The ID of the user.
        token (str): The unique session token for the user.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
    cursor.execute(
        "INSERT INTO sessions (user_id, token, created_at) VALUES (?, ?, ?)",
        (user_id, token, int(time.time()))
    )
    conn.commit()
    conn.close()

def delete_session(token: str):
    """
    Delete a session by its token, effectively logging out the user.

    Args:
        token (str): The session token to be deleted.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def validate_session(token: str) -> bool:
    """
    Validate a session token to check if it is active and not expired.

    Args:
        token (str): The session token to validate.

    Returns:
        bool: True if the session token is valid and not expired, False otherwise.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT created_at FROM sessions WHERE token = ?", (token,))
    result = cursor.fetchone()
    if result:
        created_at = result[0]
        if time.time() - created_at < SESSION_TIMEOUT:
            conn.close()
            return True
    conn.close()
    return False

def remove_expired_sessions():
    """
    Remove sessions that have expired based on the SESSION_TIMEOUT.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE created_at < ?", (int(time.time()) - SESSION_TIMEOUT,))
    conn.commit()
    conn.close()

def get_id_from_token(token: str):
    """
    Retrieve the user ID associated with a session token.

    Args:
        token (str): The session token.

    Returns:
        int or bool: The user ID if the token exists, or False if the token is invalid.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM sessions WHERE token = ?", (token,))
    result = cursor.fetchone()
    conn.close()
    return result if result else False
