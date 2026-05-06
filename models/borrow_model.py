from datetime import date, timedelta
from database.db import get_connection


class BorrowModel:

    OVERDUE_RATE = 10
    DAMAGE_FEE = 100
    LOST_FEE = 500

    # ================= CREATE BORROW =================
    @staticmethod
    def create_borrow(member_id, book_id):
        connection = get_connection()
        if not connection:
            return None

        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=3)

        cursor = connection.cursor()

        query = """
            INSERT INTO borrow_records
            (
                member_id,
                book_id,
                borrow_date,
                due_date,
                return_date,
                penalty,
                status,
                book_condition,
                condition_fee,
                late_days
            )
            VALUES (%s, %s, %s, %s, NULL, 0, 'Borrowed', 'Good', 0, 0)
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

    # ================= GET ALL BORROW RECORDS =================
    @staticmethod
    def get_all_borrow_records():
        connection = get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                br.id,
                br.member_id,
                br.book_id,
                CONCAT(u.first_name, ' ', u.last_name) AS student_name,
                b.title AS book_title,
                br.borrow_date,
                br.due_date,
                br.return_date,
                br.penalty,
                br.status,
                br.book_condition,
                br.condition_fee,
                br.late_days
            FROM borrow_records br
            INNER JOIN users u ON br.member_id = u.id
            INNER JOIN books b ON br.book_id = b.id
            ORDER BY br.id DESC
        """

        cursor.execute(query)
        records = cursor.fetchall()

        cursor.close()
        connection.close()

        return records

    # ================= GET BORROW RECORDS BY STUDENT / USER =================
    @staticmethod
    def get_borrow_records_by_student(member_id):
        connection = get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                br.id,
                br.member_id,
                br.book_id,
                b.title AS book_title,
                br.borrow_date,
                br.due_date,
                br.return_date,
                br.penalty,
                br.status,
                br.book_condition,
                br.condition_fee,
                br.late_days
            FROM borrow_records br
            INNER JOIN books b ON br.book_id = b.id
            WHERE br.member_id = %s
            ORDER BY br.id DESC
        """

        cursor.execute(query, (member_id,))
        records = cursor.fetchall()

        cursor.close()
        connection.close()

        return records

    @staticmethod
    def get_user_records(member_id):
        return BorrowModel.get_borrow_records_by_student(member_id)

    # ================= GET ACTIVE BORROW BY BOOK ID =================
    @staticmethod
    def get_active_borrow_by_book_id(book_id):
        connection = get_connection()
        if not connection:
            return None

        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                br.id,
                br.member_id,
                br.book_id,
                CONCAT(u.first_name, ' ', u.last_name) AS student_name,
                b.title AS book_title,
                br.borrow_date,
                br.due_date,
                br.return_date,
                br.penalty,
                br.status,
                br.book_condition,
                br.condition_fee,
                br.late_days
            FROM borrow_records br
            INNER JOIN users u ON br.member_id = u.id
            INNER JOIN books b ON br.book_id = b.id
            WHERE br.book_id = %s
              AND br.status = 'Borrowed'
            ORDER BY br.id DESC
            LIMIT 1
        """

        cursor.execute(query, (book_id,))
        record = cursor.fetchone()

        cursor.close()
        connection.close()

        return record

    # ================= RETURN BOOK WITH CONDITION + PENALTY =================
    @staticmethod
    def return_book(record_id, book_condition="Good"):
        if book_condition not in ["Good", "Damaged", "Lost"]:
            book_condition = "Good"

        connection = get_connection()
        if not connection:
            return None

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, book_id, due_date, status
            FROM borrow_records
            WHERE id = %s
            """,
            (record_id,)
        )

        record = cursor.fetchone()

        if not record or record["status"] != "Borrowed":
            cursor.close()
            connection.close()
            return None

        today = date.today()
        due_date = record["due_date"]

        if hasattr(due_date, "date"):
            due_date = due_date.date()

        late_days = (today - due_date).days

        if late_days > 0:
            overdue_penalty = late_days * BorrowModel.OVERDUE_RATE
        else:
            late_days = 0
            overdue_penalty = 0

        if book_condition == "Damaged":
            condition_fee = BorrowModel.DAMAGE_FEE
        elif book_condition == "Lost":
            condition_fee = BorrowModel.LOST_FEE
        else:
            condition_fee = 0

        total_penalty = overdue_penalty + condition_fee

        cursor.execute(
            """
            UPDATE borrow_records
            SET return_date = %s,
                penalty = %s,
                status = 'Returned',
                book_condition = %s,
                condition_fee = %s,
                late_days = %s
            WHERE id = %s
            """,
            (
                today,
                total_penalty,
                book_condition,
                condition_fee,
                late_days,
                record_id
            )
        )

        connection.commit()

        book_id = record["book_id"]

        cursor.close()
        connection.close()

        return {
            "book_id": book_id,
            "book_condition": book_condition,
            "condition_fee": condition_fee,
            "overdue_penalty": overdue_penalty,
            "penalty": total_penalty,
            "late_days": late_days,
            "return_date": today
        }

    # ================= COUNT BORROWED RECORDS =================
    @staticmethod
    def count_borrowed_records():
        connection = get_connection()
        if not connection:
            return 0

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM borrow_records
            WHERE status = 'Borrowed'
            """
        )

        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return count

    # ================= COUNT RETURNED RECORDS =================
    @staticmethod
    def count_returned_records():
        connection = get_connection()
        if not connection:
            return 0

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM borrow_records
            WHERE status = 'Returned'
            """
        )

        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return count