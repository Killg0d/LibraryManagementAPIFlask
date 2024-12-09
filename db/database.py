import sqlite3
from flask import current_app

def get_db_connection():
    """Establish and return a database connection."""
    database_uri = current_app.config["DATABASE_URI"]
    conn = sqlite3.connect(database_uri.split("///")[1])  # Extract file path from SQLite URI
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    """Initialize the database with required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Users table for authentication
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    
    # Create Sessions table for tokens
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT NOT NULL UNIQUE,
            created_at INTEGER NOT NULL,  -- Track when the session was created
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    # Create book table for Books
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        isbn TEXT NOT NULL UNIQUE,
        published_year INTEGER,
        genre TEXT,
        created_at INTEGER
    )

    """)

    
    conn.commit()
    conn.close()
