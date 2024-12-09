from flask import jsonify, request
from functools import wraps
from utils.auth import generate_token
from models.user import authenticate_user
from app_factory import create_app
from models.sessions import validate_session, create_session, delete_session, remove_expired_sessions
from models.book import create_book, update_book, get_all_books, get_book, delete_book, search_book
from utils.pagination import paginate

app = create_app()

def token_required(f):
    """
    A decorator to enforce token authentication for protected routes.

    Args:
        f (function): The function to wrap.

    Returns:
        function: The wrapped function if the token is valid, otherwise an error response.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"error": "Token is required"}), 400

        if not validate_session(token):
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def clean_up_expired_sessions():
    """
    Remove expired sessions from the database before handling any request.
    """
    remove_expired_sessions()

@app.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user and generate a session token.

    Returns:
        JSON response containing the session token or an error message.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user_id = authenticate_user(username, password)
    if user_id is None:
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(username)
    create_session(user_id, token)

    return jsonify({"message": "Login successful", "token": token}), 200

@app.route('/logout', methods=['POST'])
@token_required
def logout():
    """
    Log out the user by invalidating the session token.

    Returns:
        JSON response confirming the logout.
    """
    token = request.headers.get('Authorization')
    delete_session(token)
    return jsonify({"message": "Logout successful"}), 200

@app.route('/books', methods=['GET'])
def get_books():
    """
    Fetch books with optional query parameters for filtering and pagination.

    Query Parameters:
        title (str, optional): Filter by title.
        author (str, optional): Filter by author.
        isbn (str, optional): Filter by ISBN.
        genre (str, optional): Filter by genre.
        published_year (int, optional): Filter by published year.
        page (int, optional): Page number for pagination (default is 1).
        per_page (int, optional): Items per page for pagination (default is 10).

    Returns:
        JSON response containing the paginated list of books or an error message.
    """
    title = request.args.get('title')
    author = request.args.get('author')
    isbn = request.args.get('isbn')
    genre = request.args.get('genre')
    published_year = request.args.get('published_year')

    query = "SELECT * FROM books WHERE 1=1"
    params = []

    if title:
        query += " AND title LIKE ?"
        params.append(f"%{title}%")
    if author:
        query += " AND author LIKE ?"
        params.append(f"%{author}%")
    if isbn:
        query += " AND isbn = ?"
        params.append(isbn)
    if genre:
        query += " AND genre LIKE ?"
        params.append(f"%{genre}%")
    if published_year:
        query += " AND published_year = ?"
        params.append(published_year)

    rows = search_book(query, params)

    if not rows:
        return jsonify({"message": "No books found"}), 404

    books = [
        {
            'id': row[0],
            'title': row[1],
            'author': row[2],
            'isbn': row[3],
            'published_year': row[4],
            'genre': row[5],
            'created_at': row[6],
        }
        for row in rows
    ]

    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
    except ValueError:
        return jsonify({"error": "Page and per_page must be integers"}), 400

    paginated_data = paginate(books, page, per_page)

    if isinstance(paginated_data, tuple):
        return jsonify(paginated_data[0]), paginated_data[1]

    return jsonify(paginated_data), 200

@app.route('/book/<int:book_id>', methods=['GET'])
def get_single_book(book_id: int):
    """
    Fetch details of a single book by its ID.

    Args:
        book_id (int): The unique identifier of the book.

    Returns:
        JSON response containing the book details or an error message.
    """
    row = get_book(book_id)
    if row:
        book = {
            'id': row[0],
            'title': row[1],
            'author': row[2],
            'isbn': row[3],
            'published_year': row[4],
            'genre': row[5],
            'created_at': row[6]
        }
        return jsonify(book)
    return jsonify({"message": "Book not found"}), 404

@app.route('/book', methods=['POST'])
@token_required
def add_book():
    """
    Add a new book to the database.

    Returns:
        JSON response confirming the creation of the book.
    """
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    published_year = data.get('published_year')
    genre = data.get('genre')

    create_book(title, author, isbn, published_year, genre)
    return jsonify({"message": "Book created successfully"}), 201

@app.route('/book/<int:book_id>', methods=['PUT'])
@token_required
def edit_book(book_id: int):
    """
    Update the details of an existing book.

    Args:
        book_id (int): The unique identifier of the book.

    Returns:
        JSON response confirming the update of the book.
    """
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    published_year = data.get('published_year')
    genre = data.get('genre')

    update_book(book_id, title, author, isbn, published_year, genre)
    return jsonify({"message": "Book updated successfully"})

@app.route('/book/<int:book_id>', methods=['DELETE'])
@token_required
def remove_book(book_id: int):
    """
    Delete a book from the database by its ID.

    Args:
        book_id (int): The unique identifier of the book.

    Returns:
        JSON response confirming the deletion of the book.
    """
    delete_book(book_id)
    return jsonify({"message": "Book deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)