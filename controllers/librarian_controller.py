from datetime import date

from models.user_model import UserModel
from models.student_model import StudentModel
from models.book_model import BookModel
from models.borrow_model import BorrowModel

from views.manage_users_view import ManageUsersView
from views.create_user_popup_view import CreateUserPopupView


class LibrarianController:
    def __init__(self, auth_controller):
        self.auth_controller = auth_controller
        self.librarian_dashboard = None
        self.manage_users_view = None
        self.create_user_popup = None

    def set_dashboard(self, dashboard):
        self.librarian_dashboard = dashboard
        self.refresh_dashboard_stats()

    # ================= DASHBOARD =================

    def refresh_dashboard_stats(self):
        if not self.librarian_dashboard:
            return

        total_users = UserModel.count_users_by_role("student")
        total_books = BookModel.count_all_books()
        borrowed_books = BookModel.count_borrowed_books()

        records = BorrowModel.get_all_borrow_records()
        today = date.today()

        overdue_records = []
        returned_books = 0
        total_penalty = 0

        for record in records:
            penalty = float(record["penalty"]) if record["penalty"] else 0
            total_penalty += penalty

            if record["status"] == "Returned":
                returned_books += 1

            due_date = record["due_date"]

            if hasattr(due_date, "date"):
                due_date = due_date.date()

            if record["status"] == "Borrowed" and due_date < today:
                late_days = (today - due_date).days

                overdue_records.append({
                    "id": record["id"],
                    "student_name": record["student_name"],
                    "book_title": record["book_title"],
                    "borrow_date": record["borrow_date"],
                    "due_date": due_date,
                    "late_days": late_days,
                    "status": record["status"],
                    "penalty": record["penalty"]
                })

        overdue_books = len(overdue_records)

        if hasattr(self.librarian_dashboard, "set_stats"):
            self.librarian_dashboard.set_stats(
                total_users,
                total_books,
                borrowed_books,
                overdue_books
            )

        if hasattr(self.librarian_dashboard, "set_insights"):
            self.librarian_dashboard.set_insights(
                borrowed_books,
                returned_books,
                overdue_books,
                total_penalty
            )

        if hasattr(self.librarian_dashboard, "set_overdue_books"):
            self.librarian_dashboard.set_overdue_books(overdue_records)

    def logout(self):
        self.auth_controller.logout()

    # ================= NAVIGATION =================

    def open_create_user_account(self):
        self.open_create_user_popup()

    def open_create_user_popup(self):
        self.create_user_popup = CreateUserPopupView(self)
        self.create_user_popup.show()

    def open_manage_users(self):
        if self.librarian_dashboard:
            self.librarian_dashboard.hide()

        self.manage_users_view = ManageUsersView(self)
        self.manage_users_view.show()
        self.load_manage_users()

    def open_manage_books(self):
        self.auth_controller.book_controller.open_manage_books()

    def open_search_books(self):
        self.open_manage_books()

    def open_borrow_return(self):
        self.auth_controller.borrow_controller.open_borrow_return()

    # ================= CREATE USER =================

    def save_student_from_librarian(self):
        view = self.create_user_popup

        if not view:
            return

        first_name = view.first_name_input.text().strip()
        last_name = view.last_name_input.text().strip()
        email = view.email_input.text().strip()
        address = view.address_input.text().strip()
        contact_no = view.contact_input.text().strip()
        password = view.password_input.text().strip()

        if not all([first_name, last_name, email, address, contact_no, password]):
            view.show_error("Error", "Please fill in all fields.")
            return

        existing_user = UserModel.find_by_email(email)

        if existing_user:
            view.show_error("Error", "Email already exists.")
            return

        user_id = UserModel.create_user(
            first_name,
            last_name,
            email,
            address,
            password,
            "student"
        )

        if user_id:
            StudentModel.create_student(user_id, contact_no)

            view.show_message("Success", "User account created successfully.")

            view.close()
            self.create_user_popup = None

            if self.manage_users_view:
                self.load_manage_users()

            self.refresh_dashboard_stats()
        else:
            view.show_error("Error", "Failed to create user account.")

    # ================= MANAGE USERS =================

    def load_manage_users(self):
        users = UserModel.get_students_with_contact()

        if self.manage_users_view:
            self.manage_users_view.populate_table(users)

    def update_selected_user(self):
        if not self.manage_users_view:
            return

        view = self.manage_users_view

        if not view.selected_user_id:
            view.show_error("Error", "Please select a user first.")
            return

        user_id = view.selected_user_id

        first_name = view.first_name_input.text().strip()
        last_name = view.last_name_input.text().strip()
        email = view.email_input.text().strip()
        address = view.address_input.text().strip()
        contact_no = view.contact_input.text().strip()
        status = view.status_combo.currentText()

        if not all([first_name, last_name, email, address, contact_no]):
            view.show_error("Error", "Please fill in all user details.")
            return

        existing_user = UserModel.find_by_email(email)

        if existing_user and existing_user["id"] != user_id:
            view.show_error("Error", "Email already exists.")
            return

        profile_success = UserModel.update_user_basic_info(
            user_id,
            first_name,
            last_name,
            email,
            address
        )

        contact_success = StudentModel.update_student_contact(
            user_id,
            contact_no
        )

        status_success = UserModel.update_user_status(
            user_id,
            status
        )

        if profile_success and contact_success and status_success:
            view.show_message("Success", "User information updated successfully.")
            view.clear_edit_form()
            self.load_manage_users()
            self.refresh_dashboard_stats()
        else:
            view.show_error("Error", "Failed to update user information.")

    def update_selected_user_status(self):
        self.update_selected_user()

    def delete_selected_user(self):
        if not self.manage_users_view:
            return

        user_id = self.manage_users_view.selected_user_id

        if not user_id:
            self.manage_users_view.show_error("Error", "Please select a user first.")
            return

        success = UserModel.delete_user(user_id)

        if success:
            self.manage_users_view.show_message("Success", "User deleted successfully.")
            self.load_manage_users()
            self.refresh_dashboard_stats()
        else:
            self.manage_users_view.show_error("Error", "Failed to delete user.")

    def back_to_librarian_dashboard_from_users(self):
        if self.manage_users_view:
            self.manage_users_view.close()
            self.manage_users_view = None

        if self.librarian_dashboard:
            self.refresh_dashboard_stats()
            self.librarian_dashboard.show()

    # ================= CLEANUP =================

    def close_all_views(self):
        if self.manage_users_view:
            self.manage_users_view.close()
            self.manage_users_view = None

        if self.create_user_popup:
            self.create_user_popup.close()
            self.create_user_popup = None