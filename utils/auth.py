import hashlib
import os
from db.database import get_db_connection

def generate_token(username: str) -> str:
    """Generate a unique token using the username and a random salt."""
    salt = os.urandom(16).hex()
    return hashlib.sha256(f"{username}{salt}".encode()).hexdigest()

def authenticate_user(username: str, password: str) -> int:
    """Authenticate a user and return their ID if successful."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user["id"] if user else None

def save_session(user_id: int, token: str):
    """Save a new session token for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (user_id, token) VALUES (?, ?)", (user_id, token))
    conn.commit()
    conn.close()

def validate_token(token: str) -> bool:
    """Validate if a token exists in the sessions table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM sessions WHERE token = ?", (token,))
    valid = cursor.fetchone() is not None
    conn.close()
    return valid
