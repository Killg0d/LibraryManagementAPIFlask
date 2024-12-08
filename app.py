from flask import jsonify, request
from db.database import initialize_db, get_db_connection
from utils.auth import authenticate_user, generate_token, save_session
from app_factory import create_app
from models.sessions import validate_session,create_session,delete_session,remove_expired_sessions
from models.book import create_book,update_book,get_all_books,get_book,delete_book,search_book

app = create_app()

@app.before_request
def clean_up_expired_sessions():
    remove_expired_sessions()

@app.route('/login', methods=['POST'])
def login():
    """Authenticate user and generate a session token."""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    # Authenticate the user
    user_id = authenticate_user(username, password)
    if user_id is None:
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Generate and save the session token
    token = generate_token(username)
    create_session(user_id, token)
    
    return jsonify({"message": "Login successful", "token": token}), 200


@app.route('/logout', methods=['POST'])
def logout():
    """Logout the user by invalidating the session token."""
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({"error": "Token is required"}), 400
    
    # Validate the token (check if it exists in the sessions table)
    if not validate_session(token):
        return jsonify({"error": "Invalid or expired token"}), 401
    
    # Invalidate the token by deleting it from the sessions table
    delete_session(token)
    
    return jsonify({"message": "Logout successful"}), 200

@app.route('/books', methods=['GET'])
def get_books():
    """Fetch all books."""
    rows = get_all_books()
    # Convert rows into a list of dictionaries
    books = []
    for row in rows:
        book = {
            'id': row[0],
            'title': row[1],
            'author': row[2],
            'isbn': row[3],
            'published_year': row[4],
            'genre': row[5],
            'created_at': row[6]
        }
        books.append(book)
    
    return jsonify(books)

@app.route('/books/search', methods=['GET'])
def search_books():
    """Search books by title."""
    title = request.args.get('title')  # Get the title from the query parameter
    if not title:
        return jsonify({"message": "Title query parameter is required"}), 400
    
    # Use the search_book function to search the books based on title
    books = search_book(title)
    
    if books:
        # Format the results into a list of dictionaries
        result = [
            {
                'id': book[0],
                'title': book[1],
                'author': book[2],
                'isbn': book[3],
                'published_year': book[4],
                'genre': book[5],
                'created_at': book[6]
            }
            for book in books
        ]
        return jsonify(result)
    return jsonify({"message": "No books found matching the title"}), 404


@app.route('/book/<int:book_id>', methods=['GET'])
def get_single_book(book_id: int):
    """Fetch a single book by its ID."""
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
def add_book():
    """Add a new book."""
    data = request.get_json()
    
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    published_year = data.get('published_year')
    genre = data.get('genre')
    
    create_book(title, author, isbn, published_year, genre)
    return jsonify({"message": "Book created successfully"}), 201

@app.route('/book/<int:book_id>', methods=['PUT'])

def edit_book(book_id: int):
    """Update an existing book."""
    data = request.get_json()
    
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    published_year = data.get('published_year')
    genre = data.get('genre')
    
    update_book(book_id, title, author, isbn, published_year, genre)
    return jsonify({"message": "Book updated successfully"})

@app.route('/book/<int:book_id>', methods=['DELETE'])

def remove_book(book_id: int):
    """Delete a book by its ID."""
    delete_book(book_id)
    return jsonify({"message": "Book deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)