from db.database import get_db_connection
import time

def create_book(title: str, author: str, isbn: str, published_year: int, genre: str):
    """
    Create a new book record in the database.

    Args:
        title (str): The title of the book.
        author (str): The author of the book.
        isbn (str): The unique ISBN of the book.
        published_year (int): The year the book was published.
        genre (str): The genre of the book.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, author, isbn, published_year, genre, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (title, author, isbn, published_year, genre, int(time.time()))
    )
    conn.commit()
    conn.close()

def get_book(book_id: int):
    """
    Retrieve a book record by its ID.

    Args:
        book_id (int): The ID of the book to retrieve.

    Returns:
        tuple: A tuple representing the book record, or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    conn.close()
    return book

def get_all_books():
    """
    Retrieve all book records from the database.

    Returns:
        list: A list of tuples, each representing a book record.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

def search_book(query: str, params: str):
    """
    Search for books based on a custom query.

    Args:
        query (str): The SQL query to execute.
        params (str): The parameters for the query.

    Returns:
        list: A list of tuples representing books that match the query.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    books = cursor.fetchall()
    conn.close()
    return books

def update_book(book_id: int, title: str, author: str, isbn: str, published_year: int, genre: str):
    """
    Update an existing book record.

    Args:
        book_id (int): The ID of the book to update.
        title (str): The updated title of the book.
        author (str): The updated author of the book.
        isbn (str): The updated ISBN of the book.
        published_year (int): The updated publication year of the book.
        genre (str): The updated genre of the book.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE books SET title = ?, author = ?, isbn = ?, published_year = ?, genre = ? WHERE id = ?",
        (title, author, isbn, published_year, genre, book_id)
    )
    conn.commit()
    conn.close()

def delete_book(book_id: int):
    """
    Delete a book record by its ID.

    Args:
        book_id (int): The ID of the book to delete.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
