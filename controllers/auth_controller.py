from views.login_view import LoginView
from views.register_view import RegisterView
from views.admin_dashboard_view import AdminDashboardView
from views.librarian_dashboard_view import LibrarianDashboardView
from views.student_dashboard_view import StudentDashboardView

from models.user_model import UserModel
from models.student_model import StudentModel

from controllers.admin_controller import AdminController
from controllers.student_controller import StudentController
from controllers.book_controller import BookController
from controllers.borrow_controller import BorrowController
from controllers.librarian_controller import LibrarianController


class AuthController:
    def __init__(self):
        self.login_view = LoginView(self)
        self.register_view = RegisterView(self)

        self.admin_dashboard = None
        self.librarian_dashboard = None
        self.student_dashboard = None

        self.current_user = None
        self.search_books_source = None
        self.search_books_view = None

        self.admin_controller = AdminController(self)
        self.student_controller = StudentController(self)
        self.book_controller = BookController(self)
        self.borrow_controller = BorrowController(self)
        self.librarian_controller = LibrarianController(self)

    def show_login(self):
        self.login_view.show()

    def open_register(self):
        self.login_view.hide()
        self.register_view.show()

    def back_to_login(self):
        self.register_view.hide()
        self.login_view.show()

    def login(self):
        email = self.login_view.email_input.text().strip()
        password = self.login_view.password_input.text().strip()

        if not email or not password:
            self.login_view.show_error("Error", "Please fill in all fields.")
            return

        try:
            print("LOGIN CLICKED")
            user = UserModel.find_by_email_and_password(email, password)
            print("USER:", user)
        except Exception as e:
            print("LOGIN ERROR:", e)
            self.login_view.show_error("Database Error", "Unable to connect to the database.")
            return

        if not user:
            self.login_view.show_error("Login Failed", "Invalid email or password, or database unavailable.")
            return

        self.current_user = user
        self.login_view.hide()

        if user["role"] == "admin":
            self.admin_dashboard = AdminDashboardView(self.admin_controller)
            self.admin_controller.set_dashboard(self.admin_dashboard)
            self.admin_dashboard.show()

        elif user["role"] == "librarian":
            self.librarian_dashboard = LibrarianDashboardView(self.librarian_controller)
            self.librarian_controller.set_dashboard(self.librarian_dashboard)
            self.book_controller.set_librarian_dashboard(self.librarian_dashboard)
            self.borrow_controller.set_librarian_dashboard(self.librarian_dashboard)
            self.librarian_dashboard.show()

        elif user["role"] == "student":
            self.student_dashboard = StudentDashboardView(self.student_controller)
            self.student_controller.set_dashboard(self.student_dashboard)
            self.book_controller.set_student_dashboard(self.student_dashboard)
            self.student_dashboard.show()

    def logout(self):
        if self.admin_dashboard:
            self.admin_dashboard.close()
        if self.librarian_dashboard:
            self.librarian_dashboard.close()
        if self.student_dashboard:
            self.student_dashboard.close()

        self.admin_controller.close_all_views()
        self.student_controller.close_all_views()
        self.book_controller.close_all_views()
        self.borrow_controller.close_all_views()
        self.librarian_controller.close_all_views()

        self.current_user = None
        self.search_books_source = None
        self.search_books_view = None
        self.login_view.email_input.clear()
        self.login_view.password_input.clear()
        self.login_view.show()

    # ================= PUBLIC REGISTER =================

    def register_student(self):
        first_name = self.register_view.first_name_input.text().strip()
        last_name = self.register_view.last_name_input.text().strip()
        email = self.register_view.email_input.text().strip()
        address = self.register_view.address_input.text().strip()
        contact_no = self.register_view.contact_input.text().strip()
        password = self.register_view.password_input.text().strip()

        if not all([first_name, last_name, email, address, contact_no, password]):
            self.register_view.show_error("Error", "Please fill in all fields.")
            return

        try:
            existing_user = UserModel.find_by_email(email)
        except Exception as e:
            print("REGISTER CHECK ERROR:", e)
            self.register_view.show_error("Database Error", "Unable to connect to the database.")
            return

        if existing_user:
            self.register_view.show_error("Error", "Email already exists.")
            return

        try:
            user_id = UserModel.create_user(
                first_name, last_name, email, address, password, "student"
            )

            if user_id:
                StudentModel.create_student(user_id, contact_no)
                self.register_view.show_message("Success", "Student registered successfully.")
                self.register_view.hide()
                self.login_view.show()
            else:
                self.register_view.show_error("Error", "Registration failed.")
        except Exception as e:
            print("REGISTER ERROR:", e)
            self.register_view.show_error("Database Error", "Unable to save registration.")

    # ================= LIBRARIAN DELEGATES =================

    def open_create_user_account(self):
        self.librarian_controller.open_create_user_account()

    def back_to_librarian_dashboard(self):
        self.librarian_controller.back_to_librarian_dashboard()

    def save_student_from_librarian(self):
        self.librarian_controller.save_student_from_librarian()

    def open_manage_users(self):
        self.librarian_controller.open_manage_users()

    def load_manage_users(self):
        self.librarian_controller.load_manage_users()

    def delete_selected_user(self):
        self.librarian_controller.delete_selected_user()

    def back_to_librarian_dashboard_from_users(self):
        self.librarian_controller.back_to_librarian_dashboard_from_users()

    # ================= BOOK DELEGATES =================

    def open_manage_books(self):
        self.book_controller.open_manage_books()

    def load_books(self):
        self.book_controller.load_books()

    def save_book(self):
        self.book_controller.save_book()

    def update_book(self):
        self.book_controller.update_book()

    def delete_book(self):
        self.book_controller.delete_book()

    def filter_books(self):
        self.book_controller.filter_books()

    def back_to_librarian_dashboard_from_books(self):
        self.book_controller.back_to_librarian_dashboard_from_books()

    def open_search_books(self):
        self.book_controller.open_search_books_librarian()

    def load_all_books_for_search(self):
        self.book_controller.load_all_books_for_search()

    def search_books_action(self):
        self.book_controller.search_books_action()

    def back_to_librarian_dashboard_from_search(self):
        self.book_controller.back_to_librarian_dashboard_from_search()

    def back_to_student_dashboard_from_search(self):
        self.book_controller.back_to_student_dashboard_from_search()

    # ================= BORROW DELEGATES =================

    def open_borrow_return(self):
        self.borrow_controller.open_borrow_return()

    def load_borrow_return_data(self):
        self.borrow_controller.load_borrow_return_data()

    def borrow_book(self):
        self.borrow_controller.borrow_book()

    def return_selected_book(self):
        self.borrow_controller.return_selected_book()

    def back_to_librarian_dashboard_from_borrow_return(self):
        self.borrow_controller.back_to_librarian_dashboard_from_borrow_return()