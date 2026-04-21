from database.db import get_connection


class BookModel:

    @staticmethod
    def count_all_books():
        connection = get_connection()
        if not connection:
            return 0

        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM books")
        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()
        return count

    @staticmethod
    def count_available_books():
        connection = get_connection()
        if not connection:
            return 0

        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM books WHERE status = 'Available'")
        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()
        return count

    @staticmethod
    def count_borrowed_books():
        connection = get_connection()
        if not connection:
            return 0

        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM books WHERE status = 'Borrowed'")
        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()
        return count

    @staticmethod
    def get_all_books():
        connection = get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, title, author, category, status
            FROM books
            ORDER BY id ASC
        """)
        books = cursor.fetchall()

        cursor.close()
        connection.close()
        return books

    @staticmethod
    def get_books_by_status(status):
        connection = get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, title, author, category, status
            FROM books
            WHERE status = %s
            ORDER BY id ASC
        """, (status,))
        books = cursor.fetchall()

        cursor.close()
        connection.close()
        return books

    @staticmethod
    def create_book(title, author, category, status):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO books (title, author, category, status)
            VALUES (%s, %s, %s, %s)
        """, (title, author, category, status))

        connection.commit()
        cursor.close()
        connection.close()
        return True

    @staticmethod
    def update_book(book_id, title, author, category, status):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor()
        cursor.execute("""
            UPDATE books
            SET title = %s, author = %s, category = %s, status = %s
            WHERE id = %s
        """, (title, author, category, status, book_id))

        connection.commit()
        cursor.close()
        connection.close()
        return True

    @staticmethod
    def delete_book(book_id):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor()
        cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))

        connection.commit()
        cursor.close()
        connection.close()
        return True

    @staticmethod
    def set_book_status(book_id, status):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor()
        cursor.execute("""
            UPDATE books
            SET status = %s
            WHERE id = %s
        """, (status, book_id))

        connection.commit()
        cursor.close()
        connection.close()
        return True

    @staticmethod
    def get_available_books():
        connection = get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, title
            FROM books
            WHERE status = 'Available'
            ORDER BY title ASC
        """)
        books = cursor.fetchall()

        cursor.close()
        connection.close()
        return books

    @staticmethod
    def search_books(keyword):
        connection = get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)
        like = f"%{keyword}%"

        cursor.execute("""
            SELECT id, title, author, category, status
            FROM books
            WHERE title LIKE %s
               OR author LIKE %s
               OR category LIKE %s
               OR status LIKE %s
            ORDER BY id ASC
        """, (like, like, like, like))

        books = cursor.fetchall()

        cursor.close()
        connection.close()
        return books