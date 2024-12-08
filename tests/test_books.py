import random
import unittest
from app import app
from models.book import create_book, get_all_books
from db.database import get_db_connection

class BookAPITestCase(unittest.TestCase):
    """Test case for the Book API."""

    def setUp(self):
        """Set up the test database before every test."""
        # Set the app to testing mode and use the in-memory database
        app.config.from_object('config.TestingConfig')
        self.client = app.test_client()

        # Initialize the test database for each test
        self.conn = get_db_connection()
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

    def test_create_book(self):
        """Test creating a book."""
        isbn = f"1234567890-{random.randint(1000, 9999)}"  # Unique ISBN
        create_book("Test Book", "Test Author", isbn, 2024, "Fiction")
        self.cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
        book = self.cursor.fetchone()
        self.assertIsNotNone(book)

    def test_get_books(self):
        """Test fetching all books."""
        isbn = f"1234567890-{random.randint(1000, 9999)}"
        create_book("Test Book", "Test Author", isbn, 2024, "Fiction")
        books = get_all_books()
        self.assertGreater(len(books), 0)

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
        # Update the book
        self.cursor.execute("UPDATE books SET title = ? WHERE isbn = ?", ("Updated Title", isbn))
        self.conn.commit()
        self.cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
        updated_book = self.cursor.fetchone()
        self.assertEqual(updated_book[1], "Updated Title")

    def test_search_books(self):
        """Test searching books by title."""
        # Search for books by title
        isbn = f"1234567890-{random.randint(1000, 9999)}"
        create_book("Old Title", "Old Author", isbn, 2023, "Mystery")
        response = self.client.get('/books/search?title=Old')
        self.assertEqual(response.status_code, 200)

        # Check if the response contains books with 'Harry Potter' in the title
        books = response.get_json()
        self.assertGreater(len(books), 0)

        # Ensure the books have 'Harry Potter' in their title
        for book in books:
            self.assertIn('Old', book['title'])


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

if __name__ == '__main__':
    unittest.main()
