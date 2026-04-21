from PyQt6.QtWidgets import QMessageBox
from models.user_model import UserModel
from models.student_model import StudentModel
from views.create_user_account_view import CreateUserAccountView
from views.manage_users_view import ManageUsersView


class LibrarianController:
    def __init__(self, auth_controller):
        self.auth_controller = auth_controller
        self.librarian_dashboard = None
        self.create_user_account_view = None
        self.manage_users_view = None

    def set_dashboard(self, dashboard):
        self.librarian_dashboard = dashboard

    def logout(self):
        self.auth_controller.logout()

    # ================= CREATE USER =================

    def open_create_user_account(self):
        if self.librarian_dashboard:
            self.librarian_dashboard.hide()

        self.create_user_account_view = CreateUserAccountView(self)
        self.create_user_account_view.show()

    def back_to_librarian_dashboard(self):
        if self.create_user_account_view:
            self.create_user_account_view.close()
        if self.librarian_dashboard:
            self.librarian_dashboard.show()

    def save_student_from_librarian(self):
        first_name = self.create_user_account_view.first_name_input.text().strip()
        last_name = self.create_user_account_view.last_name_input.text().strip()
        email = self.create_user_account_view.email_input.text().strip()
        address = self.create_user_account_view.address_input.text().strip()
        contact_no = self.create_user_account_view.contact_input.text().strip()
        password = self.create_user_account_view.password_input.text().strip()

        if not all([first_name, last_name, email, address, contact_no, password]):
            self.create_user_account_view.show_error("Error", "Please fill in all fields.")
            return

        existing_user = UserModel.find_by_email(email)
        if existing_user:
            self.create_user_account_view.show_error("Error", "Email already exists.")
            return

        user_id = UserModel.create_user(
            first_name, last_name, email, address, password, "student"
        )

        if user_id:
            StudentModel.create_student(user_id, contact_no)
            self.create_user_account_view.show_message("Success", "Student account created successfully.")
            self.create_user_account_view.close()
            if self.librarian_dashboard:
                self.librarian_dashboard.show()
        else:
            self.create_user_account_view.show_error("Error", "Failed to create student account.")

    # ================= MANAGE USERS =================

    def open_manage_users(self):
        if self.librarian_dashboard:
            self.librarian_dashboard.hide()

        self.manage_users_view = ManageUsersView(self)
        self.manage_users_view.show()
        self.load_manage_users()

    def load_manage_users(self):
        students = UserModel.get_students_with_contact()
        if self.manage_users_view:
            self.manage_users_view.populate_table(students)

    def delete_selected_user(self):
        user_id = self.manage_users_view.selected_user_id

        if not user_id:
            self.manage_users_view.show_error("Error", "Please select a user first.")
            return

        reply = QMessageBox.question(
            self.manage_users_view,
            "Confirm Delete",
            "Are you sure you want to delete this student account?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success = UserModel.delete_user(user_id)

            if success:
                self.manage_users_view.show_message("Success", "Student account deleted successfully.")
                self.load_manage_users()
            else:
                self.manage_users_view.show_error("Error", "Failed to delete student account.")

    def back_to_librarian_dashboard_from_users(self):
        if self.manage_users_view:
            self.manage_users_view.close()
        if self.librarian_dashboard:
            self.librarian_dashboard.show()

    # ================= 🔥 IMPORTANT BRIDGES =================

    def open_manage_books(self):
        self.auth_controller.book_controller.open_manage_books()

    def open_search_books(self):
        self.auth_controller.book_controller.open_search_books_librarian()

    def open_borrow_return(self):
        self.auth_controller.borrow_controller.open_borrow_return()

    # ================= CLOSE =================

    def close_all_views(self):
        if self.create_user_account_view:
            self.create_user_account_view.close()
        if self.manage_users_view:
            self.manage_users_view.close()