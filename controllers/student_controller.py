from models.user_model import UserModel
from models.student_model import StudentModel
from models.borrow_model import BorrowModel
from views.my_borrowed_books_view import MyBorrowedBooksView
from views.edit_profile_view import EditProfileView


class StudentController:
    def __init__(self, auth_controller):
        self.auth_controller = auth_controller
        self.student_dashboard = None
        self.my_borrowed_books_view = None
        self.edit_profile_view = None

    def set_dashboard(self, dashboard):
        self.student_dashboard = dashboard

    def logout(self):
        self.auth_controller.logout()

    def open_student_borrowed_books(self):
        if self.student_dashboard:
            self.student_dashboard.hide()

        self.my_borrowed_books_view = MyBorrowedBooksView(self)
        self.my_borrowed_books_view.show()
        self.load_my_borrowed_books()

    def load_my_borrowed_books(self):
        current_user = self.auth_controller.current_user
        if not current_user:
            return

        records = BorrowModel.get_borrow_records_by_student(current_user["id"])
        if self.my_borrowed_books_view:
            self.my_borrowed_books_view.populate_table(records)

    def back_to_student_dashboard_from_borrowed_books(self):
        if self.my_borrowed_books_view:
            self.my_borrowed_books_view.close()
        if self.student_dashboard:
            self.student_dashboard.show()

    def open_student_search_books(self):
        # ✅ Use BookController, not SearchBooksView directly
        self.auth_controller.book_controller.open_search_books_student()

    def open_edit_profile(self):
        if self.student_dashboard:
            self.student_dashboard.hide()

        self.edit_profile_view = EditProfileView(self)

        current_user = self.auth_controller.current_user
        if not current_user:
            return

        user = UserModel.get_user_by_id(current_user["id"])
        student = StudentModel.get_student_by_user_id(current_user["id"])

        if user:
            self.edit_profile_view.load_data(user, student)

        self.edit_profile_view.show()

    def save_student_profile(self):
        current_user = self.auth_controller.current_user
        if not current_user:
            return

        first_name = self.edit_profile_view.first_name_input.text().strip()
        last_name = self.edit_profile_view.last_name_input.text().strip()
        email = self.edit_profile_view.email_input.text().strip()
        address = self.edit_profile_view.address_input.text().strip()
        contact_no = self.edit_profile_view.contact_input.text().strip()
        password = self.edit_profile_view.password_input.text().strip()

        if not all([first_name, last_name, email, address, contact_no, password]):
            self.edit_profile_view.show_error("Error", "Please fill in all fields.")
            return

        existing_user = UserModel.find_by_email(email)
        if existing_user and existing_user["id"] != current_user["id"]:
            self.edit_profile_view.show_error("Error", "Email already exists.")
            return

        user_updated = UserModel.update_user_profile(
            current_user["id"],
            first_name,
            last_name,
            email,
            address,
            password
        )

        student_updated = StudentModel.update_student_contact(
            current_user["id"],
            contact_no
        )

        if user_updated and student_updated:
            self.auth_controller.current_user = UserModel.get_user_by_id(current_user["id"])
            self.edit_profile_view.show_message("Success", "Profile updated successfully.")
        else:
            self.edit_profile_view.show_error("Error", "Failed to update profile.")

    def back_to_student_dashboard_from_edit_profile(self):
        if self.edit_profile_view:
            self.edit_profile_view.close()
        if self.student_dashboard:
            self.student_dashboard.show()

    def close_all_views(self):
        if self.my_borrowed_books_view:
            self.my_borrowed_books_view.close()
        if self.edit_profile_view:
            self.edit_profile_view.close()