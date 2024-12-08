from db.database import get_db_connection

class Book:
    @staticmethod
    def add(title: str, author: str, year: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all(filters=None):
        conn = get_db_connection()
        query = "SELECT * FROM books"
        params = []
        
        if filters:
            conditions = []
            if 'title' in filters:
                conditions.append("title LIKE ?")
                params.append(f"%{filters['title']}%")
            if 'author' in filters:
                conditions.append("author LIKE ?")
                params.append(f"%{filters['author']}%")
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        
        cursor = conn.cursor()
        cursor.execute(query, params)
        books = cursor.fetchall()
        conn.close()
        return [dict(book) for book in books]

    @staticmethod
    def get_by_id(book_id: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        book = cursor.fetchone()
        conn.close()
        return dict(book) if book else None

    @staticmethod
    def update(book_id: int, title: str, author: str, year: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?",
            (title, author, year, book_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(book_id: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()
