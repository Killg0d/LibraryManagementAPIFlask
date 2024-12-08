import time
from db.database import get_db_connection

SESSION_TIMEOUT = 3600  # Session expiration time in seconds (e.g., 1 hour)

def create_session(user_id: int, token: str):
    """Create a session for the user and save it in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Delete any existing session for the user to enforce one active session per user
    cursor.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
    
    # Insert the new session
    cursor.execute(
        "INSERT INTO sessions (user_id, token, created_at) VALUES (?, ?, ?)",
        (user_id, token, int(time.time()))  # Store the current timestamp
    )
    
    conn.commit()
    conn.close()

def delete_session(token: str):
    """Delete a session by its token (log out)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Delete the session where the token matches
    cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
    
    conn.commit()
    conn.close()

def validate_session(token: str) -> bool:
    """Check if the session token is valid (exists in the database and not expired)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the session exists and is not expired
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
    """Remove expired sessions periodically."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Remove sessions that are older than SESSION_TIMEOUT
    cursor.execute("DELETE FROM sessions WHERE created_at < ?", (int(time.time()) - SESSION_TIMEOUT,))
    
    conn.commit()
    conn.close()
