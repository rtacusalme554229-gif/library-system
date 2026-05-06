from database.db import get_connection


class StudentModel:

    @staticmethod
    def create_student(user_id, contact_no):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO students (user_id, contact_no)
            VALUES (%s, %s)
            """,
            (user_id, contact_no)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return True

    @staticmethod
    def get_student_by_user_id(user_id):
        connection = get_connection()
        if not connection:
            return None

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, user_id, contact_no
            FROM students
            WHERE user_id = %s
            """,
            (user_id,)
        )

        student = cursor.fetchone()

        cursor.close()
        connection.close()

        return student

    @staticmethod
    def update_student_contact(user_id, contact_no):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM students
            WHERE user_id = %s
            """,
            (user_id,)
        )

        existing = cursor.fetchone()

        if existing:
            cursor.execute(
                """
                UPDATE students
                SET contact_no = %s
                WHERE user_id = %s
                """,
                (contact_no, user_id)
            )
        else:
            cursor.execute(
                """
                INSERT INTO students (user_id, contact_no)
                VALUES (%s, %s)
                """,
                (user_id, contact_no)
            )

        connection.commit()

        cursor.close()
        connection.close()

        return True