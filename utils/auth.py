import hashlib
import os

def generate_token(username: str) -> str:
    """Generate a unique token using the username and a random salt."""
    salt = os.urandom(16).hex()
    return hashlib.sha256(f"{username}{salt}".encode()).hexdigest()
