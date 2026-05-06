from database.db import get_connection


class UserModel:

    # ================= FIND USER BY EMAIL + PASSWORD =================
    @staticmethod
    def find_by_email_and_password(email, password):
        connection = get_connection()
        if not connection:
            return None

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, first_name, last_name, email, address, password, role, status
            FROM users
            WHERE email = %s AND password = %s
            """,
            (email, password)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        return user

    # ================= FIND USER BY EMAIL =================
    @staticmethod
    def find_by_email(email):
        connection = get_connection()
        if not connection:
            return None

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, first_name, last_name, email, address, password, role, status
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        return user

    # ================= GET USER BY ID =================
    @staticmethod
    def get_user_by_id(user_id):
        connection = get_connection()
        if not connection:
            return None

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, first_name, last_name, email, address, password, role, status
            FROM users
            WHERE id = %s
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        return user

    # ================= CREATE USER =================
    @staticmethod
    def create_user(first_name, last_name, email, address, password, role):
        connection = get_connection()
        if not connection:
            return None

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users
            (first_name, last_name, email, address, password, role, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'Active')
            """,
            (first_name, last_name, email, address, password, role)
        )

        connection.commit()
        user_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return user_id

    # ================= CREATE LIBRARIAN =================
    @staticmethod
    def create_librarian(first_name, last_name, email, address, password):
        return UserModel.create_user(
            first_name,
            last_name,
            email,
            address,
            password,
            "librarian"
        )

    # ================= GET USERS BY ROLE =================
    @staticmethod
    def get_users_by_role(role):
        connection = get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, first_name, last_name, email, address, role, status
            FROM users
            WHERE role = %s
            ORDER BY id ASC
            """,
            (role,)
        )

        users = cursor.fetchall()

        cursor.close()
        connection.close()

        return users

    # ================= GET ALL USERS =================
    @staticmethod
    def get_all_users():
        connection = get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, first_name, last_name, email, address, role, status
            FROM users
            ORDER BY id ASC
            """
        )

        users = cursor.fetchall()

        cursor.close()
        connection.close()

        return users

    # ================= GET STUDENTS WITH CONTACT NO =================
    @staticmethod
    def get_students_with_contact():
        connection = get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT u.id,
                   u.first_name,
                   u.last_name,
                   u.email,
                   u.address,
                   u.role,
                   u.status,
                   COALESCE(s.contact_no, '') AS contact_no
            FROM users u
            LEFT JOIN students s ON u.id = s.user_id
            WHERE u.role = 'student'
            ORDER BY u.id ASC
            """
        )

        users = cursor.fetchall()

        cursor.close()
        connection.close()

        return users

    # ================= COUNT USERS BY ROLE =================
    @staticmethod
    def count_users_by_role(role):
        connection = get_connection()
        if not connection:
            return 0

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM users
            WHERE role = %s
            """,
            (role,)
        )

        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return count

    # ================= UPDATE LIBRARIAN INFO =================
    @staticmethod
    def update_librarian(user_id, first_name, last_name, email, address):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET first_name = %s,
                last_name = %s,
                email = %s,
                address = %s
            WHERE id = %s AND role = 'librarian'
            """,
            (first_name, last_name, email, address, user_id)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return True

    # ================= UPDATE STUDENT / USER BASIC INFO =================
    @staticmethod
    def update_user_basic_info(user_id, first_name, last_name, email, address):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET first_name = %s,
                last_name = %s,
                email = %s,
                address = %s
            WHERE id = %s AND role = 'student'
            """,
            (first_name, last_name, email, address, user_id)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return True

    # ================= UPDATE USER STATUS =================
    @staticmethod
    def update_user_status(user_id, new_status):
        if new_status not in ["Active", "Inactive"]:
            return False

        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET status = %s
            WHERE id = %s
            """,
            (new_status, user_id)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return True

    # ================= UPDATE USER PROFILE =================
    @staticmethod
    def update_user_profile(user_id, first_name, last_name, email, address, password):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET first_name = %s,
                last_name = %s,
                email = %s,
                address = %s,
                password = %s
            WHERE id = %s
            """,
            (first_name, last_name, email, address, password, user_id)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return True

    # ================= DELETE LIBRARIAN =================
    @staticmethod
    def delete_librarian(user_id):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM users
            WHERE id = %s AND role = 'librarian'
            """,
            (user_id,)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return True

    # ================= DELETE USER / STUDENT =================
    @staticmethod
    def delete_user(user_id):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM users
            WHERE id = %s AND role = 'student'
            """,
            (user_id,)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return True