from db.database import initialize_db, get_db_connection
from flask import Flask
def create_app():
    """Application factory to create and configure the Flask app."""
    app = Flask(__name__)

    # Initialize the database
    with app.app_context():
        initialize_db()
        add_test_user()

    return app

def add_test_user():
    """Add a test user to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", 
                   ("testuser", "testpassword"))
    conn.commit()
    conn.close()