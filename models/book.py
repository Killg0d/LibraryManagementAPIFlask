from db.database import get_db_connection
import time

def create_book(title: str, author: str, isbn: str, published_year: int, genre: str):
    """Create a new book record in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert the new book
    cursor.execute(
        "INSERT INTO books (title, author, isbn, published_year, genre, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (title, author, isbn, published_year, genre, int(time.time()))  # Store current timestamp
    )
    
    conn.commit()
    conn.close()

def get_book(book_id: int):
    """Get a book by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    
    conn.close()
    return book

def get_all_books():
    """Get all books in the system."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    
    conn.close()
    return books

def search_book(title: str):
    """Search books using the title."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Use parameterized queries to avoid SQL injection
    cursor.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + title + '%',))
    books = cursor.fetchall()

    conn.close()
    return books


def update_book(book_id: int, title: str, author: str, isbn: str, published_year: int, genre: str):
    """Update the details of an existing book."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE books SET title = ?, author = ?, isbn = ?, published_year = ?, genre = ? WHERE id = ?",
        (title, author, isbn, published_year, genre, book_id)
    )
    
    conn.commit()
    conn.close()

def delete_book(book_id: int):
    """Delete a book by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    
    conn.commit()
    conn.close()
