import random
import unittest
from models.book import create_book, get_all_books
from db.database import get_db_connection
from app_factory import create_app
from flask import current_app
class BookDatabaseTestCase(unittest.TestCase):
    """Test case for the Book API."""

    def setUp(self):
        """Set up the test database before every test."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        # Manually push the application context to make sure we can access app's config
        self.app_context = self.app.app_context()
        self.app_context.push()
        # Initialize the test database for each test
        self.conn = get_db_connection()  # Pass the database URI here
        self.cursor = self.conn.cursor()

        # Create the books table for each test
        self.cursor.execute("""
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
        self.conn.commit()

    def tearDown(self):
        """Clean up the database after every test."""
        # Drop the books table after each test
        self.cursor.execute("DROP TABLE IF EXISTS books")
        self.conn.commit()
        self.conn.close()
        # Pop the application context after the test is done
        self.app_context.pop()
    
    def test_database_connection(self):
        """Verify the test database is being used."""
        with self.app.app_context():
            db_uri = current_app.config['DATABASE_URI']
            self.assertIn('sqlite:///test_database.db', db_uri)


    def test_create_book(self):
        """Test creating a book."""
        isbn = f"1234567890-{random.randint(1000, 9999)}"  # Unique ISBN
        create_book("Test Book", "Test Author", isbn, 2024, "Fiction")
        self.cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
        book = self.cursor.fetchone()
        self.assertIsNotNone(book)
        
    def test_get_single_book(self):
        """Test fetching a single book by its ISBN."""
        isbn = f"1234567890-{random.randint(1000, 9999)}"
        create_book("Test Book", "Test Author", isbn, 2024, "Fiction")
        self.cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
        book = self.cursor.fetchone()
        self.assertIsNotNone(book)
        self.assertEqual(book[3], isbn)

    def test_update_book(self):
        """Test updating an existing book."""
        isbn = f"1234567890-{random.randint(1000, 9999)}"
        create_book("Old Title", "Old Author", isbn, 2023, "Mystery")
        self.cursor.execute("UPDATE books SET title = ? WHERE isbn = ?", ("Updated Title", isbn))
        self.conn.commit()
        self.cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
        updated_book = self.cursor.fetchone()
        self.assertEqual(updated_book[1], "Updated Title")
    

    def test_delete_book(self):
        """Test deleting a book."""
        isbn = f"1234567890-{random.randint(1000, 9999)}"
        create_book("Book to be deleted", "Author", isbn, 2022, "Non-fiction")
        # Delete the book
        self.cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
        self.conn.commit()
        self.cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
        deleted_book = self.cursor.fetchone()
        self.assertIsNone(deleted_book)

    def test_get_books(self):
        isbn = f"1234567890-{random.randint(1000, 9999)}"
        create_book("Test Book", "Test Author", isbn, 2024, "Fiction")
        self.cursor.execute("SELECT * FROM books")
        book = self.cursor.fetchall()
        self.assertIsNotNone(book)

if __name__ == '__main__':
    unittest.main()
