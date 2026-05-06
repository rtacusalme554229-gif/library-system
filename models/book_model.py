from database.db import get_connection


class BookModel:

    # ================= HELPER: COMPUTE STATUS =================
    @staticmethod
    def compute_status(available_copies, borrowed_copies, lost_copies):
        if available_copies > 0:
            return "Available"

        if borrowed_copies > 0:
            return "Borrowed"

        if lost_copies > 0:
            return "Lost"

        return "Available"

    # ================= ADD BOOK =================
    @staticmethod
    def add_book(title, author, category, total_copies):
        connection = get_connection()
        if not connection:
            return None

        cursor = connection.cursor()

        total_copies = int(total_copies)
        if total_copies < 1:
            total_copies = 1

        cursor.execute(
            """
            INSERT INTO books
            (title, author, category, total_copies, available_copies, borrowed_copies, lost_copies, status)
            VALUES (%s, %s, %s, %s, %s, 0, 0, 'Available')
            """,
            (title, author, category, total_copies, total_copies)
        )

        connection.commit()
        book_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return book_id

    # ================= GET ALL BOOKS =================
    @staticmethod
    def get_all_books():
        connection = get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, title, author, category, status,
                   total_copies, available_copies, borrowed_copies, lost_copies
            FROM books
            ORDER BY id ASC
            """
        )

        books = cursor.fetchall()

        cursor.close()
        connection.close()

        return books

    # ================= GET BOOK BY ID =================
    @staticmethod
    def get_book_by_id(book_id):
        connection = get_connection()
        if not connection:
            return None

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, title, author, category, status,
                   total_copies, available_copies, borrowed_copies, lost_copies
            FROM books
            WHERE id = %s
            """,
            (book_id,)
        )

        book = cursor.fetchone()

        cursor.close()
        connection.close()

        return book

    # ================= SEARCH BOOKS =================
    @staticmethod
    def search_books(keyword):
        connection = get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)

        search_value = f"%{keyword}%"

        cursor.execute(
            """
            SELECT id, title, author, category, status,
                   total_copies, available_copies, borrowed_copies, lost_copies
            FROM books
            WHERE title LIKE %s
               OR author LIKE %s
               OR category LIKE %s
               OR status LIKE %s
            ORDER BY id ASC
            """,
            (search_value, search_value, search_value, search_value)
        )

        books = cursor.fetchall()

        cursor.close()
        connection.close()

        return books

    # ================= GET BOOKS BY STATUS =================
    @staticmethod
    def get_books_by_status(status):
        connection = get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, title, author, category, status,
                   total_copies, available_copies, borrowed_copies, lost_copies
            FROM books
            WHERE status = %s
            ORDER BY id ASC
            """,
            (status,)
        )

        books = cursor.fetchall()

        cursor.close()
        connection.close()

        return books

    # ================= UPDATE BOOK INFO + COPIES =================
    @staticmethod
    def update_book(book_id, title, author, category, total_copies):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT borrowed_copies, lost_copies
            FROM books
            WHERE id = %s
            """,
            (book_id,)
        )

        book = cursor.fetchone()

        if not book:
            cursor.close()
            connection.close()
            return False

        borrowed_copies = int(book["borrowed_copies"] or 0)
        lost_copies = int(book["lost_copies"] or 0)
        total_copies = int(total_copies)

        minimum_total = borrowed_copies + lost_copies

        if total_copies < minimum_total:
            cursor.close()
            connection.close()
            return False

        available_copies = total_copies - borrowed_copies - lost_copies
        status = BookModel.compute_status(
            available_copies,
            borrowed_copies,
            lost_copies
        )

        cursor.execute(
            """
            UPDATE books
            SET title = %s,
                author = %s,
                category = %s,
                total_copies = %s,
                available_copies = %s,
                status = %s
            WHERE id = %s
            """,
            (
                title,
                author,
                category,
                total_copies,
                available_copies,
                status,
                book_id
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return True

    # ================= BORROW ONE COPY =================
    @staticmethod
    def borrow_one_copy(book_id):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT available_copies, borrowed_copies, lost_copies
            FROM books
            WHERE id = %s
            """,
            (book_id,)
        )

        book = cursor.fetchone()

        if not book:
            cursor.close()
            connection.close()
            return False

        available_copies = int(book["available_copies"] or 0)
        borrowed_copies = int(book["borrowed_copies"] or 0)
        lost_copies = int(book["lost_copies"] or 0)

        if available_copies <= 0:
            cursor.close()
            connection.close()
            return False

        available_copies -= 1
        borrowed_copies += 1

        status = BookModel.compute_status(
            available_copies,
            borrowed_copies,
            lost_copies
        )

        cursor.execute(
            """
            UPDATE books
            SET available_copies = %s,
                borrowed_copies = %s,
                status = %s
            WHERE id = %s
            """,
            (available_copies, borrowed_copies, status, book_id)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return True

    # ================= RETURN ONE COPY =================
    @staticmethod
    def return_one_copy(book_id, condition):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT available_copies, borrowed_copies, lost_copies
            FROM books
            WHERE id = %s
            """,
            (book_id,)
        )

        book = cursor.fetchone()

        if not book:
            cursor.close()
            connection.close()
            return False

        available_copies = int(book["available_copies"] or 0)
        borrowed_copies = int(book["borrowed_copies"] or 0)
        lost_copies = int(book["lost_copies"] or 0)

        if borrowed_copies <= 0:
            cursor.close()
            connection.close()
            return False

        borrowed_copies -= 1

        if condition == "Lost":
            lost_copies += 1
        else:
            available_copies += 1

        status = BookModel.compute_status(
            available_copies,
            borrowed_copies,
            lost_copies
        )

        cursor.execute(
            """
            UPDATE books
            SET available_copies = %s,
                borrowed_copies = %s,
                lost_copies = %s,
                status = %s
            WHERE id = %s
            """,
            (
                available_copies,
                borrowed_copies,
                lost_copies,
                status,
                book_id
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return True

    # ================= DELETE BOOK =================
    @staticmethod
    def delete_book(book_id):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT borrowed_copies
            FROM books
            WHERE id = %s
            """,
            (book_id,)
        )

        book = cursor.fetchone()

        if not book:
            cursor.close()
            connection.close()
            return False

        if int(book["borrowed_copies"] or 0) > 0:
            cursor.close()
            connection.close()
            return False

        cursor.execute(
            """
            DELETE FROM books
            WHERE id = %s
            """,
            (book_id,)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return True

    # ================= COUNTS =================
    @staticmethod
    def count_all_books():
        connection = get_connection()
        if not connection:
            return 0

        cursor = connection.cursor()

        cursor.execute("SELECT COALESCE(SUM(total_copies), 0) FROM books")
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

        cursor.execute("SELECT COALESCE(SUM(available_copies), 0) FROM books")
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

        cursor.execute("SELECT COALESCE(SUM(borrowed_copies), 0) FROM books")
        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return count