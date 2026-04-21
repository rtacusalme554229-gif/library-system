from database.db import get_connection


class UserModel:
    @staticmethod
    def find_by_email_and_password(email, password):
        connection = get_connection()
        if not connection:
            return None

        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT * FROM users
            WHERE email = %s AND password = %s
        """
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        cursor.close()
        connection.close()
        return user

    @staticmethod
    def find_by_email(email):
        connection = get_connection()
        if not connection:
            return None

        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        cursor.close()
        connection.close()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        connection = get_connection()
        if not connection:
            return None

        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT id, first_name, last_name, email, address, password, role
            FROM users
            WHERE id = %s
        """
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()

        cursor.close()
        connection.close()
        return user

    @staticmethod
    def create_user(first_name, last_name, email, address, password, role):
        connection = get_connection()
        if not connection:
            return None

        cursor = connection.cursor()
        query = """
            INSERT INTO users (first_name, last_name, email, address, password, role)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (first_name, last_name, email, address, password, role))
        connection.commit()
        user_id = cursor.lastrowid

        cursor.close()
        connection.close()
        return user_id

    @staticmethod
    def create_librarian(first_name, last_name, email, address, password):
        connection = get_connection()
        if not connection:
            return None

        cursor = connection.cursor()
        query = """
            INSERT INTO users (first_name, last_name, email, address, password, role)
            VALUES (%s, %s, %s, %s, %s, 'librarian')
        """
        cursor.execute(query, (first_name, last_name, email, address, password))
        connection.commit()
        user_id = cursor.lastrowid

        cursor.close()
        connection.close()
        return user_id

    @staticmethod
    def update_user_profile(user_id, first_name, last_name, email, address, password):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor()
        query = """
            UPDATE users
            SET first_name = %s,
                last_name = %s,
                email = %s,
                address = %s,
                password = %s
            WHERE id = %s
        """
        cursor.execute(query, (first_name, last_name, email, address, password, user_id))
        connection.commit()

        cursor.close()
        connection.close()
        return True

    @staticmethod
    def get_users_by_role(role):
        connection = get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT id, first_name, last_name, email, address, role
            FROM users
            WHERE role = %s
            ORDER BY id ASC
        """
        cursor.execute(query, (role,))
        users = cursor.fetchall()

        cursor.close()
        connection.close()
        return users

    @staticmethod
    def count_users_by_role(role):
        connection = get_connection()
        if not connection:
            return 0

        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM users WHERE role = %s"
        cursor.execute(query, (role,))
        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()
        return count

    @staticmethod
    def get_students_with_contact():
        connection = get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                users.id,
                users.first_name,
                users.last_name,
                users.email,
                users.address,
                students.contact_no
            FROM users
            LEFT JOIN students ON users.id = students.user_id
            WHERE users.role = 'student'
            ORDER BY users.first_name ASC, users.last_name ASC
        """
        cursor.execute(query)
        students = cursor.fetchall()

        cursor.close()
        connection.close()
        return students

    @staticmethod
    def delete_user(user_id):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor()
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        connection.commit()

        cursor.close()
        connection.close()
        return True

    @staticmethod
    def update_librarian(user_id, first_name, last_name, email, address):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor()
        query = """
            UPDATE users
            SET first_name = %s,
                last_name = %s,
                email = %s,
                address = %s
            WHERE id = %s AND role = 'librarian'
        """
        cursor.execute(query, (first_name, last_name, email, address, user_id))
        connection.commit()

        cursor.close()
        connection.close()
        return True

    @staticmethod
    def delete_librarian(user_id):
        connection = get_connection()
        if not connection:
            return False

        cursor = connection.cursor()
        query = "DELETE FROM users WHERE id = %s AND role = 'librarian'"
        cursor.execute(query, (user_id,))
        connection.commit()

        cursor.close()
        connection.close()
        return True

    @staticmethod
    def get_all_users():
        connection = get_connection()
        if not connection:
            return []

        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT id, first_name, last_name, email, address, role
            FROM users
            ORDER BY id ASC
        """
        cursor.execute(query)
        users = cursor.fetchall()

        cursor.close()
        connection.close()
        return users