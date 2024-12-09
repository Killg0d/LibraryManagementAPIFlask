## Book Management API (Flask)

This README.md file provides instructions on running and using a simple Flask API for managing books.

### Overview

This project offers a basic API for managing books. It includes:

* User authentication with session management
* CRUD operations (Create, Read, Update, Delete) for book records
* Built with Flask, SQLite, and JWT for authentication

### How to Run the Project

**Prerequisites:**

* Python 3.7 or higher
* Flask
* SQLite (or configured database URI)

**Setup:**

1. Clone the repository:

```bash
git clone https://github.com/Killg0d/LibraryManagementAPIFlask.git
```

2. Navigate to the project directory:

```bash
cd LibraryManagementAPIFlask
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure Database URI (in `config.py`):

```python
class DevelopmentConfig:
    DATABASE_URI = "sqlite:///dev.db"
```

   - Replace `sqlite:///dev.db` with your preferred database connection string if using a different database.

5. Initialize the Database:

   The database will automatically be initialized when the application runs.

6. Run the application:

```bash
python app.py
```

   This will start the Flask application accessible at `http://localhost:5000`.

### API Endpoints

**Authentication:**

* `POST /login`: Authenticates a user and returns a session token.
* `POST /logout` (requires authentication): Logs out the user by invalidating their session token.

**Book Management:**

* `GET /books` (optional filtering & pagination): Retrieves a list of books.
* `GET /book/<int:book_id>`: Retrieves details of a specific book by its ID.
* `POST /book` (requires authentication): Creates a new book.
* `PUT /book/<int:book_id>` (requires authentication): Updates an existing book.
* `DELETE /book/<int:book_id>` (requires authentication): Deletes a book by its ID.

**Code Example (GET /books):**

```python
import requests

url = "http://localhost:5000/books"
response = requests.get(url)

if response.status_code == 200:
  data = response.json()
  print(f"Retrieved {len(data['books'])} books!")
  for book in data['books']:
      print(f" - {book['title']}")
else:
  print(f"Error retrieving books: {response.status_code}")
```

### Design Choices

* **Flask Application Factory:** 
   The `create_app` function creates and configures the Flask application based on the environment (development, testing, production).
* **Database Initialization:** 
   Handled within `create_app` to ensure the database is set up before the application starts.
* **Token Authentication:** 
   JWT-based for securing routes requiring user login. The `token_required` decorator checks for a valid token before granting access.
* **Database Interaction:** 
   Uses SQLite and the `get_db_connection` function establishes a connection for querying.
* **Pagination:** 
   The `paginate` function handles pagination for the `/books` endpoint.

### Assumptions and Limitations

**Assumptions:**

* Valid user input (e.g., username, password) is provided.
* Designed for small-scale applications using SQLite. For larger production systems, consider a more robust database like PostgreSQL or MySQL.

**Limitations:**

* Current implementation uses SQLite, not recommended for high-concurrency or production environments.
* Authentication tokens are stored in memory, invalidating all sessions when the application restarts.
* No email verification or password recovery system.
* Basic pagination; lacks advanced features like sorting or filtering by multiple fields.

### Contributing

Feel free to fork the repository and submit pull requests with improvements or new features!
