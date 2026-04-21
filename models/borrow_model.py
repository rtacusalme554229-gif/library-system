from datetime import date, timedelta
from database.db import get_connection


class BorrowModel:
    @staticmethod
    def create_borrow(member_id, book_id):
        connection = get_connection()
        if not connection:
            return None

        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=3)

        cursor = connection.cursor()
        query = """
            INSERT INTO borrow_records (member_id, book_id, borrow_date, due_date, return_date, penalty, status)
            VALUES (%s, %s, %s, %s, NULL, 0, 'Borrowed')
        """
        cursor.execute(query, (member_id, book_id, borrow_date, due_date))
        connection.commit()

        record_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return {
            "record_id": record_id,
            "member_id": member_id,
            "book_id": book_id,
            "borrow_date": borrow_date,
            "due_date": due_date,
            "status": "Borrowed"
        }

    @staticmethod
    def get_all_borrow_records():
        connection = get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT
                borrow_records.id,
                borrow_records.member_id,
                borrow_records.book_id,
                CONCAT(users.first_name, ' ', users.last_name) AS student_name,
                books.title AS book_title,
                borrow_records.borrow_date,
                borrow_records.due_date,
                borrow_records.return_date,
                borrow_records.penalty,
                borrow_records.status
            FROM borrow_records
            INNER JOIN users ON borrow_records.member_id = users.id
            INNER JOIN books ON borrow_records.book_id = books.id
            ORDER BY borrow_records.id DESC
        """
        cursor.execute(query)
        records = cursor.fetchall()

        cursor.close()
        connection.close()
        return records

    @staticmethod
    def get_borrow_records_by_student(member_id):
        connection = get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT
                borrow_records.id,
                borrow_records.member_id,
                borrow_records.book_id,
                books.title AS book_title,
                borrow_records.borrow_date,
                borrow_records.due_date,
                borrow_records.return_date,
                borrow_records.penalty,
                borrow_records.status
            FROM borrow_records
            INNER JOIN books ON borrow_records.book_id = books.id
            WHERE borrow_records.member_id = %s
            ORDER BY borrow_records.id DESC
        """
        cursor.execute(query, (member_id,))
        records = cursor.fetchall()

        cursor.close()
        connection.close()
        return records

    @staticmethod
    def return_book(record_id):
        connection = get_connection()
        if not connection:
            return None

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, book_id, due_date, status FROM borrow_records WHERE id = %s",
            (record_id,)
        )
        record = cursor.fetchone()

        if not record or record["status"] == "Returned":
            cursor.close()
            connection.close()
            return None

        today = date.today()
        due_date = record["due_date"]
        late_days = (today - due_date).days

        penalty = late_days * 10 if late_days > 0 else 0
        status = "Returned"

        update_query = """
            UPDATE borrow_records
            SET return_date = %s, penalty = %s, status = %s
            WHERE id = %s
        """
        cursor.execute(update_query, (today, penalty, status, record_id))
        connection.commit()

        book_id = record["book_id"]

        cursor.close()
        connection.close()

        return {
            "book_id": book_id,
            "penalty": penalty,
            "return_date": today
        }